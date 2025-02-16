import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv  
from pathlib import Path
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


@app.get("/test")
async def test_ws():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Chat</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            #chatbox { width: 80%; height: 300px; border: 1px solid black; overflow-y: scroll; margin: 20px auto; padding: 10px; }
            #message { width: 70%; padding: 10px; }
            #send { padding: 10px; }
        </style>
    </head>
    <body>
        <h2>Chatbot WebSocket Test</h2>
        <div id="chatbox"></div>
        <input type="text" id="message" placeholder="Type a message..." />
        <button id="send">Send</button>

        <script>
            const ws = new WebSocket("ws://localhost:8000/wsc");

            ws.onopen = function() {
                console.log("Connected to WebSocket");
                document.getElementById("chatbox").innerHTML += "<p><b>Connected to server</b></p>";
            };

            ws.onmessage = function(event) {
                const chatbox = document.getElementById("chatbox");
                const lastMessage = chatbox.lastElementChild;

                try {
                    const data = JSON.parse(event.data); // Parse JSON response
                    const messagePart = data.part || ""; // Extract streamed message part
                    
                    if (lastMessage && lastMessage.classList.contains("server-message")) {
                        lastMessage.innerHTML += messagePart; // Append chunk
                    } else {
                        let newMessage = document.createElement("p");
                        newMessage.classList.add("server-message");
                        newMessage.innerHTML = "<b>Server:</b> " + messagePart;
                        chatbox.appendChild(newMessage);
                    }
                    
                    chatbox.scrollTop = chatbox.scrollHeight; // Auto-scroll to latest message
                } catch (error) {
                    console.error("Error parsing WebSocket message:", error);
                }
            };

            ws.onclose = function() {
                document.getElementById("chatbox").innerHTML += "<p><b>Connection closed</b></p>";
            };

            function sendMessage() {
                const messageInput = document.getElementById("message");
                const chatbox = document.getElementById("chatbox");
                const message = messageInput.value.trim();

                if (message) {
                    ws.send(JSON.stringify({ text: message }));
                    chatbox.innerHTML += "<p><b>You:</b> " + message + "</p>";
                    messageInput.value = "";
                }
            }

            document.getElementById("send").onclick = sendMessage;
            
            // Allow pressing "Enter" to send message
            document.getElementById("message").addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)