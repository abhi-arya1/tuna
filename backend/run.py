import uvicorn 
from dotenv import load_dotenv  
from pathlib import Path

load_dotenv(Path(__file__).parent / ".env")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )