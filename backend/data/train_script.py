import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    TrainerCallback,
    TrainerState,
    TrainerControl,
)
from peft import LoraConfig, get_peft_model
from pathlib import Path
import json
from typing import Dict
from huggingface_hub import login

with open("/home/ubuntu/runway/secrets.txt") as f:
    login(token=f.read().strip())

class CustomCallback(TrainerCallback):
    def __init__(self):
        self.step = 0
        
    def log(self, msg):
        print(msg, flush=True)

    def on_log(self, args, state: TrainerState, control: TrainerControl, logs: Dict[str, float] = None, **kwargs):
        if logs is not None:
            self.step += 1
            log_str = f"Step {self.step}: "
            metrics = []
            for key, value in logs.items():
                if isinstance(value, (int, float)):
                    metrics.append(f"{key}: {value:.4f}")
            log_str += ", ".join(metrics)
            self.log(log_str)
    
    def on_init_end(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        self.log("Initialization completed")
        return control

    def on_train_begin(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        self.log("Training started")
        return control

    def on_train_end(self, args, state: TrainerState, control: TrainerControl, **kwargs):
        self.log("Training completed")
        return control

def main():
    logger = CustomCallback()
    
    # Set memory efficiency configurations
    logger.log("Setting up memory optimizations...")
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    torch.cuda.empty_cache()

    try:
        # Load Dataset
        logger.log("Loading dataset...")
        train_dataset = load_dataset(
            'json', 
            data_files='/home/ubuntu/runway/dataset.jsonl', 
            split='train'
        )
        logger.log(f"Loaded dataset with {len(train_dataset)} examples")
        logger.log(f"Dataset features: {train_dataset.features}")

        # Load Tokenizer
        logger.log("Loading tokenizer...")
        model_name = "meta-llama/Llama-3.1-8B"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        logger.log("Tokenizer loaded successfully")

        # Modified tokenization approach
        logger.log("Starting dataset tokenization...")
        def tokenize_function(examples):
            prompts = []
            for i in range(len(examples['input'])):
                prompt = f"input: {examples['input'][i]}\noutput: {examples['output'][i]}"
                prompts.append(prompt)
            
            return tokenizer(
                prompts,
                truncation=True,
                max_length=128,
                padding=False,
                return_tensors=None
            )

        # Process dataset
        train_dataset = train_dataset.map(
            tokenize_function,
            batched=True,
            batch_size=8,
            remove_columns=train_dataset.column_names,
            desc="Tokenizing dataset"
        )

        # Set the format after tokenization
        train_dataset.set_format(type="torch")
        logger.log("Dataset tokenization complete")

        # Data Collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )

        # Load Base Model
        logger.log("Loading base model with memory optimizations...")
        base_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        logger.log("Base model loaded successfully")

        # Configure LoRA
        logger.log("Configuring LoRA...")
        peft_config = LoraConfig(
            r=8,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
            target_modules=["q_proj", "v_proj"]
        )

        peft_model = get_peft_model(base_model, peft_config)
        
        if hasattr(peft_model, "enable_input_require_grads"):
            peft_model.enable_input_require_grads()
        peft_model.gradient_checkpointing_enable()

        trainable_params = sum(p.numel() for p in peft_model.parameters() if p.requires_grad)
        logger.log(f"PEFT model prepared with {trainable_params} trainable parameters")

        # Training Arguments
        logger.log("Setting up training arguments...")
        training_args = TrainingArguments(
            output_dir="runway_lora",
            overwrite_output_dir=True,
            num_train_epochs=20,
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            learning_rate=5e-5,
            eval_strategy="no",  # Updated from evaluation_strategy
            logging_strategy="steps",
            logging_steps=1,
            save_strategy="epoch",
            save_total_limit=2,
            fp16=True,
            optim="adamw_torch_fused",
            gradient_checkpointing=True,
            max_grad_norm=0.3,
        )

        # Create Trainer and Train
        trainer = Trainer(
            model=peft_model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
            callbacks=[logger]
        )

        logger.log("Starting model training...")
        trainer.train()
        
        logger.log("Training complete, saving model...")
        trainer.save_model()
        
        print("Training completed successfully.", flush=True)

    except Exception as e:
        error_msg = f"Error during training: {str(e)}"
        print(f"[ERROR] {error_msg}", flush=True)
        raise e

if __name__ == "__main__":
    main()