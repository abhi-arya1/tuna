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

Welcome to a new Tuna Notebook! In this notebook, we will be training a {base_model} model using the Tuna CLI.

## 1. Dependencies 

We're going to start by installing all of our tuning dependencies directly onto the machine.
""", NbType.MARKDOWN),


        # Requirements Install
        JupyterBlock("""
# Only run this once per instance
print("Installing Dependencies...")
!pip install -q -U transformers peft accelerate datasets bitsandbytes
!pip install -q -U scipy ipywidgets matplotlib numpy torch
print("Finished installing dependencies!")
""", NbType.CODE),


        # Status Description
        JupyterBlock(f"""
Now that we've finished installing the necessary libraries, we can move on to the next step.

## 2. Model Configuration
                     
In this section, we'll be configuring the model of choice, {base_model}, for training.
This includes setting up the model constants, system configuration, and other necessary details.
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
    target_modules=["q_proj", "k_proj", "v_proj"],
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
""", NbType.MARKDOWN),

        JupyterBlock(f"""
print("Using Model: {base_model}")

from torch import bfloat16
from transformers import (
    AutoModelForCausalLM,
    BitsAndBytesConfig
)
                     
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
print("=" * 70)
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

lengths = plot_data_lengths(tokenized_train_dataset, tokenized_val_dataset)
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
""", NbType.CODE)

    ]

    return blocks
