import uvicorn 
from dotenv import load_dotenv  
from pathlib import Path
from os import getenv

load_dotenv(Path(__file__).parent / ".env")

if __name__ == "__main__":
    if(getenv("ENV_LOADED") != "true"):
        raise Exception("Environment variables not loaded")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )