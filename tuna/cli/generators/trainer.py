"""

Tuna Notebook Generation Service

"""

from tuna.cli.util.block import JupyterBlock


def _block_1():
    def markdown(model: str) -> str:
        return f"# Tuna {model} Trainer"

    code = """
import os 
import traceback 
import typing 
import dataclasses 
import torch 
import transformers 
import datasets
import peft
import trl 
"""

    return JupyterBlock(markdown, code, 1)
