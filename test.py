from torch import bfloat16

print("Using Model: mistralai/Mistral-7B-v0.3")

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
    "google/gemma-2-9b",
    # quantization_config=BITS_N_BYTES_CFG,
    token="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"
)
