import asyncio, paramiko
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv  
from pathlib import Path
from os import getenv
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse
from core.response import respond
from sdks.hf import get_models, get_model
from util.dtypes import WSRequest
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(Path(__file__).parent / ".env")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT"],
    allow_headers=["*"],
)

active_socket: WebSocket | None = None 

@app.get("/")
async def read_root():
    return JSONResponse({"message": "Welcome to the Tuna API"}, status_code=200)

@app.get('/models')
async def get_model_list():
    return { "models": get_models() }

@app.get('/dataset')
async def get_dataset():
    with open("data/dataset.jsonl", "r") as file:
        return JSONResponse(content={
            "dataset": file.read().splitlines()
        }, status_code=200)
    


@app.post("/v1/chat/completions")
async def generate(request: ChatRequest):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(username="ubuntu", hostname=getenv("SSH_HOST_H100"))

        
        
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.websocket("/wsc")
async def websocket_endpoint(websocket: WebSocket):
    global active_socket

    await websocket.accept()
    active_socket = websocket
    print("WebSocket connection established")

    try:
        while True:
            data = await websocket.receive_json()
            data = WSRequest(**data)
            await respond(data, websocket.send_json)
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    finally:
        active_socket = None

