import asyncio
from typing import Any, AsyncGenerator, Callable, Literal
from sdks.groqapi import groq as client
from util.models import GroqModels

async def build_response(data: Any, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    async for chunk in await client.chat.completions.create(
        model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
        messages=[{"role": "user", "content": data["text"]}],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    ):
        content = chunk.choices[0].delta.content
        print(content)
        await send_handler({"part": content or ""})



async def respond():
    pass
