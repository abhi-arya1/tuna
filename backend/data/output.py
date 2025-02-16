from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch
import uvicorn

class ChatRequest(BaseModel):
    prompt: str
    max_length: int = 1000
    temperature: float = 0.7
    top_p: float = 0.9

class ChatResponse(BaseModel):
    generated_text: str

app = FastAPI()

def load_model():
    base_model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-3.1-8B",
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Load the LoRA adapter
    model = PeftModel.from_pretrained(
        base_model,
        "/home/ubuntu/runway/runway_lora",
        adapter_name="default"
    )
    
    model = model.merge_and_unload()
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
    return model, tokenizer


model, tokenizer = load_model()

@app.post("/v1/chat/completions")
async def generate(request: ChatRequest):
    try:
        inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
        
        outputs = model.generate(
            **inputs,
            max_length=request.max_length,
            temperature=request.temperature,
            top_p=request.top_p,
            pad_token_id=tokenizer.eos_token_id
        )
        
        response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return ChatResponse(generated_text=response_text)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)