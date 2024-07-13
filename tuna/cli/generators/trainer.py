# pylint: disable=all

import os
import torch
import transformers 
import datasets
import peft
import trl

from dotenv import load_dotenv
load_dotenv()

class TunaTrainer:
    def __init__(self, base_model: str, model_path: str, device: torch.device):
        self.base_model = base_model
        self.model_path = model_path
        self.device = device
        self.model

    
    @staticmethod
    def _setup_model(base_model: str):
        pass
