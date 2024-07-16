"""
This module contains the functions to generate the markdown 
and code blocks for the notebook.
"""

# pylint: disable=line-too-long

from os import remove
import inquirer
from halo import Halo
from tuna.cli.core.constants import \
    R_OUTPUT_MODEL, R_MODEL_ADAPTERS, NOTEBOOK, LEARN, INFO_ICON, R_TUNA_DIR, R_TRAIN_DATA, R_EVAL_DATA
from tuna.util.nbutil import JupyterBlock, NbType, add_md_cell, add_code_cell, validate_nb
from tuna.util.general import log

INFO_ICON = "ⓘ"

def make_notebook():
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
        inquirer.Text("base_model", message=f"Enter the base model for the new notebook. {LEARN('base_model')}"),
        inquirer.Text("base_prompt", message=f"Enter the base prompt for the new model. {LEARN('base_prompt')}")
    ]
    answers = inquirer.prompt(questions)
    base_model = answers["base_model"]
    base_prompt = answers["base_prompt"]
    blocks = get_nb(base_model, base_prompt)

    spinner = Halo(text="Generating Notebook", spinner="dots")
    spinner.start()
    for block in blocks:
        if block.blocktype() == NbType.MARKDOWN:
            add_md_cell(NOTEBOOK, block.blockcontent())
        else:
            add_code_cell(NOTEBOOK, block.blockcontent())

    spinner.succeed("Notebook Generated Successfully!")


def get_nb(
    base_model: str,
    base_prompt: str
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
!pip install -q -U bitsandbytes
!pip install -q -U git+https://github.com/huggingface/transformers.git
!pip install -q -U git+https://github.com/huggingface/peft.git
!pip install -q -U git+https://github.com/huggingface/accelerate.git
!pip install -q -U datasets scipy ipywidgets matplotlib
!pip install -q -U torch
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
MODEL_PATH = "{R_OUTPUT_MODEL}"
ADAPTERS   = "{R_MODEL_ADAPTERS}"

# Get HuggingFace Token 
with open("{R_TUNA_DIR}/auth.config.json", 'r') as f:
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
print(f"[{INFO_ICON}] Model saving to: {R_OUTPUT_MODEL}")
print(f"[{INFO_ICON}] Adapters saving to : {R_MODEL_ADAPTERS}")
print(f"[{INFO_ICON}] Compute Device: {{DEVICE}}")
print("=" * 70)
""", NbType.CODE),


        # Model Training Setup
        JupyterBlock("""
## 3. Model Training Setup 
                     
We'll now configure the model with HuggingFace, set up the training data, and prepare the model for training.
This includes tokenizing, dataset building, and more!
""", NbType.MARKDOWN),

        JupyterBlock("""
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
                     
BITS_N_BYTES_CFG = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
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

with open("{R_TRAIN_DATA}", 'r') as train, \
     open("{R_EVAL_DATA}", 'r') as eval:
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
    ]

    return blocks
