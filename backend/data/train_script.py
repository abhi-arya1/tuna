import os
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model
from pathlib import Path

def main():
    # --------------------------------------------------------------------------
    # 1. Load Dataset
    # Replace "your-dataset-name" with the actual dataset name on Hugging Face
    # If your dataset is a local JSON file or local dataset, adjust accordingly.
    # The dataset must have columns "input" and "output".
    # --------------------------------------------------------------------------
    train_dataset = load_dataset('json', data_files='/home/ubuntu/runway/dataset.jsonl', split='train') 

    # --------------------------------------------------------------------------
    # 2. Choose a Pretrained Model and Tokenizer
    # --------------------------------------------------------------------------
    model_name = "meta-llama/Llama-3.1-8B"  
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token  # ensure pad_token is set

    # --------------------------------------------------------------------------
    # 3. Tokenize
    # We'll combine 'input' and 'output' into a single text sequence,
    # for example: "input: <user_input>\noutput: <gold_output>"
    # Adjust the prompt format as needed.
    # --------------------------------------------------------------------------
    def tokenize_function(example):
        prompt = f"input: {example['input']}\noutput: {example['output']}"
        return tokenizer(
            prompt,
            padding="max_length",
            max_length=128,
            truncation=True,
        )

    train_dataset = train_dataset.map(tokenize_function, batched=False)

    # We only need the input_ids and attention_mask from tokenized output
    train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

    # --------------------------------------------------------------------------
    # 4. Prepare Data Collator for Language Modeling
    # --------------------------------------------------------------------------
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=False  # For causal language modeling, mlm=False
    )

    # --------------------------------------------------------------------------
    # 5. Load Base Model
    # --------------------------------------------------------------------------
    base_model = AutoModelForCausalLM.from_pretrained(model_name)

    # --------------------------------------------------------------------------
    # 6. Configure LoRA
    # LoraConfig can be adjusted. Below is a minimal example:
    # --------------------------------------------------------------------------
    peft_config = LoraConfig(
        r=8,                      # rank
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"     # important: sets the correct LoRA task
    )

    # Convert base model to a LoRA PEFT model
    peft_model = get_peft_model(base_model, peft_config)
    print("PEFT Model:", peft_model)

    # --------------------------------------------------------------------------
    # 7. Define Training Arguments
    # Adjust output_dir, epochs, batch sizes, etc. as needed.
    # --------------------------------------------------------------------------
    training_args = TrainingArguments(
        output_dir="runway_lora",
        overwrite_output_dir=True,
        num_train_epochs=20,  # More epochs due to tiny dataset
        per_device_train_batch_size=1,  # Ensure model sees all data
        per_device_eval_batch_size=1,  # If eval set exists
        learning_rate=5e-5,  # Slightly lower LR to prevent overfitting
        evaluation_strategy="no",  # No eval if no validation set
        logging_strategy="steps",
        logging_steps=1,  # Log every step for small dataset
        save_strategy="epoch",  # Save at every epoch
        save_total_limit=2,
        fp16=torch.cuda.is_available()
    )

    # --------------------------------------------------------------------------
    # 8. Create Trainer and Train
    # --------------------------------------------------------------------------
    trainer = Trainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
    )

    print("Starting model training...")
    trainer.train()
    trainer.save_model()


if __name__ == "__main__":
    main()
