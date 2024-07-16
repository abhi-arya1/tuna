"""

This module contains the functions to generate the markdown 
and code blocks for the notebook.

"""

# pylint: disable=line-too-long

from os import remove
import inquirer
from halo import Halo
from tuna.cli.core.constants import \
    OUTPUT_MODEL, ADAPTERS, NOTEBOOK, LEARN, INFO_ICON, TUNA_LAB_LOC
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
        inquirer.Text("base_model", message=f"Enter the base model for the new notebook. {LEARN("base_model")}"),
    ]
    answers = inquirer.prompt(questions)
    base_model = answers["base_model"]
    blocks = get_nb(base_model)

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
""", NbType.MARKDOWN),


# Requirements Install
        JupyterBlock("""
# Installing Dependencies 
                     
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

# Model Configuration
                     
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
MODEL_PATH = "{OUTPUT_MODEL}"
ADAPTERS   = "{ADAPTERS}"

# Get HuggingFace Token 
with open("{TUNA_LAB_LOC}/auth.config.json", 'r') as f:
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
print("[{INFO_ICON}] Base Model: {base_model}")
print("[{INFO_ICON}] Model saving to: {OUTPUT_MODEL}")
print("[{INFO_ICON}] Adapters saving to : {ADAPTERS}")
print(f"[{INFO_ICON}] Compute Device: {{DEVICE}}")
print("=================" + "=" * 70)

""", NbType.CODE),


# Model Training Setup
        JupyterBlock("""
# Model Training Setup 
                     
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
    ]

    return blocks
