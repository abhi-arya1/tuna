import asyncio, paramiko, json, time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from dotenv import load_dotenv  
from pathlib import Path
from os import getenv
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, StreamingResponse
from core.response import respond
from sdks.hf import get_models, get_model
from util.dtypes import WSRequest, ChatCompletionRequest, ChatCompletionResponse, Message
from util.helpers import stream_from_ssh
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
async def create_chat_completion(request: ChatCompletionRequest):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            hostname=getenv("SSH_HOST_H100"),
            username="ubuntu",
            key_filename=getenv("SSH_KEY_PATH")
        )

        command = (
            'source /home/ubuntu/runway/.venv/bin/activate && '
            'python3 /home/ubuntu/runway/output.py'
        )
        stdin, stdout, stderr = ssh.exec_command(command)
        
        json_request = json.dumps(request.dict())
        stdin.write(json_request)
        stdin.channel.shutdown_write()
        
        output = stdout.read().decode("utf-8")
        # print(f"<<{output.strip()}>>")
        ssh.close()
        
        response_data = json.loads(output)
        # print(f"<<{response_data}>>")
        return JSONResponse(response_data)
    except Exception as e:
        print(e)
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

