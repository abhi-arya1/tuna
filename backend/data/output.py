import sys
import json
import torch
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from datetime import datetime

# Basic logging setup
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('/home/ubuntu/model_server.log'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )
#logger = logging.get#logger(__name__)

def load_model():
    #logger.info("Loading base model: meta-llama/Llama-3.1-8B")
    base_model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.1-8B",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    #logger.info("Loading LoRA adapter from /home/ubuntu/runway/runway_lora")
    model = PeftModel.from_pretrained(
        base_model,
        "/home/ubuntu/runway/runway_lora",
        adapter_name="default"
    )
    #logger.info("Merging and unloading model")
    model = model.merge_and_unload()
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
    #logger.info("Model loading complete")
    return model, tokenizer

def format_chat_prompt(messages):
    prompt = ""
    for message in messages:
        role = message["role"]
        content = message["content"]
        prompt += f"{role.capitalize()}: {content}\n"
    prompt += "Assistant: "
    return prompt

def generate_response(model, tokenizer, messages, max_tokens=1000, temperature=0.7, top_p=0.9):
    prompt = format_chat_prompt(messages)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output_ids = model.generate(
        **inputs,
        max_length=inputs.input_ids.shape[1] + max_tokens,
        temperature=temperature,
        top_p=top_p,
        pad_token_id=tokenizer.eos_token_id
    )
    full_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Remove the prompt from the generated text
    response_text = full_text[len(prompt):].strip()
    return response_text

#logger.info("Loading model...")
model, tokenizer = load_model()
#logger.info("Model server ready to process requests")

# Read the entire JSON request from standard input
input_str = sys.stdin.read()
if not input_str:
    #logger.error("No input received.")
    sys.exit(1)

try:
    request = json.loads(input_str)
    messages = request.get("messages", [])
    max_tokens = request.get("max_tokens", 1000)
    temperature = request.get("temperature", 0.7)
    top_p = request.get("top_p", 0.9)
    
    #logger.info("Generating response...")
    response_text = generate_response(model, tokenizer, messages, max_tokens, temperature, top_p)
    #logger.info(f"Response generated: {response_text}")
    
    # Build the full response in one go
    response = {
        "id": "chatcmpl-" + str(hash(response_text))[:8],
        "created": int(datetime.now().timestamp()),
        "model": "runway-lora",
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": response_text
            },
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": -1,
            "completion_tokens": -1,
            "total_tokens": -1
        }
    }
    #logger.info("Response ready to send", response)
    print(json.dumps(response), flush=True)
except Exception as e:
    #logger.error(f"Error processing request: {str(e)}", exc_info=True)
    error_response = {
        "error": {
            "message": str(e),
            "type": "internal_error"
        }
    }
    print(json.dumps(error_response), flush=True)
