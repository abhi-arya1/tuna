from groq import AsyncGroq 
from os import getenv 

groq = AsyncGroq(api_key=getenv("GROQ_API_KEY"))
