from groq import AsyncGroq, Groq
from os import getenv 

groq = AsyncGroq(api_key=getenv("GROQ_API_KEY"))
syncgroq = Groq(api_key=getenv("GROQ_API_KEY"))
