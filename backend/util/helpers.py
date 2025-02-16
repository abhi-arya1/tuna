import json, asyncio
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import HTTPException

def make_json_serializable(data):
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    return data


def get_time_for_log(): 
    return datetime.now().strftime("%H:%M:%S")


def get_log_format(msg: str, tuna_msg: bool = False):
    if tuna_msg:
        return f"<<{get_time_for_log()}>> [TUNA] {msg}...\n"
    else: 
        return f"<<{get_time_for_log()}>> {msg}"



async def stream_from_ssh(ssh_client, channel, request_data):
    try:
        # Send request to the model server
        print("HERE2")
        channel.send(json.dumps(request_data) + "\n")
        print("HERE")
        
        buffer = ""
        while True:
            if channel.recv_ready():
                chunk = channel.recv(4096).decode('utf-8')
                buffer += chunk
                
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    print(line)
                    try:
                        response = json.loads(line)
                        if "error" in response:
                            raise Exception(response["error"]["message"])
                        yield f"data: {json.dumps(response)}\n\n"
                    except json.JSONDecodeError:
                        continue
                        
            await asyncio.sleep(0.01)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    yield "data: [DONE]\n\n"