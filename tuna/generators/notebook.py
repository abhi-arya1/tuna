"""
This module contains the functions to generate the markdown 
and code blocks for the notebook.
"""

# pylint: disable=line-too-long
from os import remove
import inquirer
from halo import Halo
from tuna.cli.core.constants import \
    R_OUTPUT_MODEL, R_MODEL_ADAPTERS, NOTEBOOK, LEARN, INFO_ICON, \
    R_TRAIN_DATA, R_EVAL_DATA, OUTPUT_MODEL, MODEL_ADAPTERS, TRAIN_DATA, \
    EVAL_DATA, AUTH_FILE, R_AUTH_FILE
from tuna.util.nbutil import JupyterBlock, NbType, add_md_cell, add_code_cell, validate_nb
from tuna.util.general import log, validate_non_empty


INFO_ICON = "ⓘ"


def _pick_paths(local: bool) -> tuple[str, str, str, str, str]:
    """
    Returns the paths for the notebook generation.
    """
    if local:
        return OUTPUT_MODEL, MODEL_ADAPTERS, AUTH_FILE, TRAIN_DATA, EVAL_DATA
    return R_OUTPUT_MODEL, R_MODEL_ADAPTERS, R_AUTH_FILE, R_TRAIN_DATA, R_EVAL_DATA




def make_notebook(local=False):
    """
    Makes a new notebook given a base model prompt.
    """
    if validate_nb(NOTEBOOK):
        questions = [
            inquirer.Confirm("overwrite", message="A notebook already exists. Overwrite?", default=False)
        ]
        answers = inquirer.prompt(questions)
        if not answers["overwrite"]:
            return
        remove(NOTEBOOK)
        log(INFO_ICON, f"Notebook {NOTEBOOK} removed successfully!")

    questions = [
        inquirer.Text("base_model", message=f"Enter the base model for the new notebook. {LEARN('base_model')}", validate=validate_non_empty, default="mistralai/Mistral-7B-v0.3"),
        inquirer.Text("base_prompt", message=f"Enter the base prompt for the new model. {LEARN('base_prompt')}", validate=validate_non_empty)
    ]
    answers = inquirer.prompt(questions)
    base_model = answers["base_model"]
    base_prompt = answers["base_prompt"]
    output_path, adapters, auth, train, eval_path = _pick_paths(local)
    blocks = get_nb(
        base_model,
        base_prompt,
        output_path,
        adapters,
        auth,
        train,
        eval_path
    )

    spinner = Halo(text="Generating Notebook", spinner="dots")
    spinner.start()
    for block in blocks:
        if block.blocktype() == NbType.MARKDOWN:
            add_md_cell(NOTEBOOK, block.blockcontent())
        else:
            add_code_cell(NOTEBOOK, block.blockcontent())

    spinner.succeed(f"Tuna Notebook for '{base_model}' Generated Successfully!")




# pylint: disable=too-many-arguments
def get_nb(
    base_model: str,
    base_prompt: str,
    output_path: str,
    model_adapters: str,
    auth_file: str,
    train_file: str,
    eval_file: str
) -> list[JupyterBlock]:
    """
    Generates the markdown and code blocks for the notebook.

    Args:
        base_model (str): The base model to use for the notebook.
        model_type (str): The type of model to use for the notebook.

    Returns:
        list[str]: A list of markdown and code blocks for the notebook.
    """

    blocks = [

        # Opening Title
        JupyterBlock(f"""
# Tuna {base_model} Trainer

Welcome to a new Tuna Notebook! In this notebook, we will be training a {base_model} model using the Tuna interface.

As we're training a CAUSAL_LM (Cause-and-Effect/Call-and-Response LLM), we'll be using LoRA (Low-Rank Adaptation) and PEFT (Parameter-Efficient Fine-Tuning)
to train a minimal amount of parameters in a cost-effective manner, while still getting comparable results to foundational models trained on the same data. 

Interested in learning more? Check out the QLoRA Paper on ArXiV: https://arxiv.org/abs/2305.14314

## 1. Dependencies 

We're going to start by installing all of our tuning dependencies directly onto the machine.
""", NbType.MARKDOWN),


        # Requirements Install
        JupyterBlock("""
# Only run this once per instance
print("Installing Dependencies...")
!pip install -U transformers peft accelerate datasets bitsandbytes
!pip install -U scipy ipywidgets matplotlib numpy==1.26.4 torch
print("Finished installing dependencies!")
""", NbType.CODE),


        # Status Description
        JupyterBlock(f"""
Now that we've finished installing the necessary libraries, we can move on to the next step.

## 2. Model Configuration
                     
In this section, we'll be configuring the model of choice, {base_model}, for training.
This includes setting up the model constants, system configuration, and other necessary details.

Let's quickly go through what the Lora Config means: 

- `r`: Rank of the matrix used, controlling the parameters trained. More provides more detail, but uses more compute. 
- `lora_alpha` = `alpha`: Scaling factor, i.e. how much the LoRA weights affect the model, scaled by `alpha/r`

LoRA usually uses `alpha=16` and `r=64` parameters, but you can adjust these for your use cases. For example, 
`r=32` and `alpha=64` allows for more emphasis on the fine-tuning with reduced computation, but this is up to you.

- `target_modules` are the vector projections that this training is going to target. For more information, read: 
- `bias=none` states that the model won't bias any data in its training, though this can be set to `all` (all bias) or `lora_only` (biased towards training)
- `lora_dropout=0.05` states that 5% of the trained activations will be dropped during training, to avoid an overfitting of data. 
- `task_type` is the type of task you're training for. Models that are text generators usually fall under `CAUSAL_LM`, as a large language model.
""", NbType.MARKDOWN),


        # Model Configuration
        JupyterBlock(f"""
import json
import torch
from peft import LoraConfig
       
# Model Constants 
BASE_MODEL = "{base_model}"
MODEL_PATH = "{output_path}"
ADAPTERS   = "{model_adapters}"

# Get HuggingFace Token 
with open("{auth_file}", 'r') as f:
    data = json.load(f)
HF_TOKEN = data.get('hf_api_key', None)

# System Configuration

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
elif torch.xpu.is_available():
    DEVICE = torch.device("xpu")
else:
    DEVICE = torch.device("cpu")

LORA_CONFIG = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "lm_head",
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

print("= TRAINER CONFIG " + "=" * 70)
print(f"[{INFO_ICON}] Base Model: {base_model}")
print(f"[{INFO_ICON}] Model saving to: {output_path}")
print(f"[{INFO_ICON}] Adapters saving to : {model_adapters}")
print(f"[{INFO_ICON}] Compute Device: {{DEVICE}}")
print("=" * 70)
""", NbType.CODE),


        # Model Training Setup
        JupyterBlock("""
## 3. Model Training Setup 
                     
We'll now configure the model with HuggingFace, set up the training data, and prepare the model for training.
This includes tokenizing, dataset building, and more!
                     
If we have more than one GPU, we'll be using parallel processing to make everything faster!
We'll end by printing out the model to see what we're working with, and how many parameters we can train.
""", NbType.MARKDOWN),

        JupyterBlock(f"""
print("Using Model: {base_model}")

from torch import bfloat16
from transformers import (
    AutoModelForCausalLM,
    BitsAndBytesConfig
)
from peft import get_peft_model
                     
BITS_N_BYTES_CFG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=bfloat16,
    bnb_4bit_use_double_quant=True
)

MODEL = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=BITS_N_BYTES_CFG,
    token=HF_TOKEN
)

# If >1 GPU and using GPU training (no CPU/XPU)
if DEVICE == "cuda" and torch.cuda.device_count() > 1:
    MODEL.is_parallelizable = True
    MODEL.model_parallel = True


def print_Lora_stats(model):
    trainable_params = 0
    all_param = 0
    for _, param in model.named_parameters():
        all_param += param.numel()
        if param.requires_grad:
            trainable_params += param.numel()
    print(
        f"Trainable Parameters: {{trainable_params}} | All Parameters: {{all_param}} | Trainable %: {{100 * trainable_params / all_param}}"
    )

MODEL = get_peft_model(MODEL, LORA_CONFIG)
print(MODEL)
print_Lora_stats(MODEL)
""", NbType.CODE),


        # Dataset Setup
        JupyterBlock("""
## 4. Dataset Setup 
                     
In this section, we'll be setting up the generated dataset for training.
""", NbType.MARKDOWN),

        JupyterBlock(f"""
from json import load
from datasets import Dataset

with open("{train_file}", 'r') as train, \
     open("{eval_file}", 'r') as eval:
    train_data = json.load(train)
    eval_data = json.load(eval)          

train_dataset = Dataset.from_dict(train_data)
eval_dataset = Dataset.from_dict(eval_data)

# Function to format training examples as prompts
def formatting_func(example):
    text = f"### User: {base_prompt}. Prompt: {{example['text']}} Answer: {{example['label']}}"
    return {{"text": text}}

train_r, train_c = train_dataset.shape()
eval_r, eval_c = eval_dataset.shape()
""", NbType.CODE),

        JupyterBlock("""
## 5. Tokenization and Dataset Information

We'll set up the tokenizer and print out some information about the dataset.
We added padding on the left, as [the training uses less memory this way](https://ai.stackexchange.com/questions/41485/while-fine-tuning-a-decoder-only-llm-like-llama-on-chat-dataset-what-kind-of-pa).
""", NbType.MARKDOWN),

        JupyterBlock(f"""
from transformers import AutoTokenizer
                     
tokenizer = AutoTokenizer.from_pretrained(
    "{base_model}",
    padding_side="left",
    add_eos_token=True,
    add_bos_token=True
)
tokenizer.pad_token = tokenizer.eos_token

def generate_and_tokenize(prompt):
    return tokenizer(formatting_func(prompt))
                     
train_dataset = train_dataset.map(generate_and_tokenize)
eval_dataset = eval_dataset.map(generate_and_tokenize)

print("= DATASET INFORMATION " + "=" * 70)
print(f"[{INFO_ICON}] Training Dataset: {{train_r}} rows, {{train_c}} columns, {{train_dataset.size_in_bytes() // (2**30)}} GB")
print(f"[{INFO_ICON}] Evaluation Dataset: {{eval_r}} rows, {{eval_c}} columns, {{eval_dataset.size_in_bytes() // (2**30)}} GB")
print("======================" + "=" * 70)
""", NbType.CODE),

        JupyterBlock("""
### 5.5. Dataset Validation 

We're now going to make a distribution of our dataset's lengths, which'll provide
us with a better understanding of the dataset's structure. The graph below will plot the 
`max_length` of the input tokens, which will let us truncate to max length.
""", NbType.MARKDOWN),

        JupyterBlock("""
import matplotlib.pyplot as plt 
                     
def plot_data(train_set, eval_set): 
    lengths = [len(x['input_ids']) for x in train_set]
    lengths += [len(x['input_ids']) for x in eval_set]

    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=20, alpha=0.7, color='blue')
    plt.title("Distribution of lengths of \'input_ids\' in the Dataset")
    plt.xlabel("Length of input_ids")
    plt.ylabel("Frequency")
    plt.show()
                     
plot_data(train_dataset, eval_dataset)
""", NbType.CODE),

        JupyterBlock("""
import numpy as np

def calculate_max_length(lengths, percentile=95):
    max_length = int(np.percentile(lengths, percentile))
    print(f"Calculated max_length at {percentile}th percentile: {max_length}")
    return max_length

lengths = plot_data_lengths(train_dataset, eval_dataset)
max_length = calculate_max_length(lengths, percentile=95)

def clean_prompts(prompt, max_length):
    result = tokenizer(
        formatting_func(prompt),
        truncation=True,
        max_length=max_length,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result
                     
# We'll map the new tokenized inputs back to the dataset 
train_dataset = train_dataset.map(clean_prompts)
eval_dataset = eval_dataset.map(clean_prompts)
                     
# And finally, we'll make sure the data lenghts are normalized.
plot_data_lengths(train_dataset, eval_dataset)
""", NbType.CODE),

        JupyterBlock(f"""
## 6. Baseline Evaluation 
                     
We're now going to give the base model, {base_model}, a chance to 
prove its abilities out-of-the-box.

For example, if I was tuning a bot to have a lot of context on my code repository, I can ask it something of the form below:

```python 
eval_prompt = \"\"\"Fix this issue for my repository: Issue for long load times in app/page.tsx\"\"\"
```

This should ideally give you a generalized output, ready for upgrades, and we recommend keeping this example prompt simple.
""", NbType.MARKDOWN),

        JupyterBlock(f"""
example_tokenizer = AutoTokenizer.from_pretrained(
    "{base_model}",
    add_bos_token=True
)

example_prompt = str(input("Enter your evaluation prompt: "))

model_input = example_tokenizer(example_prompt, return_tensors="pt").to(f"{{DEVICE}}")
model.eval()

with torch.no_grad():
    response = eval_tokenizer.decode(model.generate**model_input, max_new_tokens=256, repetition_penalty=1.15)[0], skip_special_tokens=True))
    print("= BASELINE EVALUATION " + "=" * 70)
    print(f"[{INFO_ICON}] Prompt: {{example_prompt}}")
    print(f"[{INFO_ICON}] Baseline Response from {base_model}: {{response)}}")
    print("======================" + "=" * 70)
""", NbType.CODE),

        JupyterBlock("""
## 7. Training
                     
Let's train our model. You can configure steps based on how intensive you want your tuning to be. 
Note that the smaller your dataset, the less tuned your model will be unfortunately.
                     
#### 7.1. A Note on Overfit
                     
Overfitting a model is when the model is training well, but unable to infer further, because it's too restricted.
When a model overfits significantly, it's important to shut off the training. We set `max_steps=250` below, but you can set this low or high, 
based on whether you want to deal with this or not. 
                     
**Make sure to monitor your trainer**, since when training loss goes down (good), and validation loss goes up (bad), you have reached overfit.
You can interrupt the training process by clicking `Kernel > Interrupt Kernel` in the Navbar, and the `peft` library will save all previous checkpoints for you, and you can load the best checkpoint.
                     
Let's do it 🔥
""", NbType.MARKDOWN),

        JupyterBlock("""
from transformers import Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datetime import datetime
                     
PROJECT = str(input("Enter a project name: "))

TUNA_TRAINER = Trainer(
    model=MODEL,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    args=TrainingArguments(
        output_dir=MODEL_PATH
        warmup_steps=2,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=1,
        gradient_checkpointing=True,
        max_steps=250,
        learning_rate=2.5e-5, # Want a small lr for finetuning
        bf16=True,
        optim="paged_adamw_8bit",
        logging_steps=25,            
        logging_dir="./logs",        
        save_strategy="steps",       
        save_steps=50,                
        evaluation_strategy="steps", 
        eval_steps=50,               
        # do_eval=True, # Remove the comments to use WandB for Evaluation
        # report_to="wandb", 
        # run_name=f"{{PROJECT}}-{{BASE_MODEL}}-{{datetime.now().strftime('%Y-%m-%d-%H-%M')}}
    )
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)
                     
MODEL.config.use_cache = False
TUNA_TRAINER.train()
""", NbType.CODE),

        JupyterBlock("""
## 8. Run the Model
                     
We're done training (Hopefully)! We'll find that out for sure after trying it out. We're going to have to reload the model


""", NbType.MARKDOWN)
    ]

    return blocks
