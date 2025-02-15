import asyncio
from typing import Any, Callable, Literal
from sdks.groqapi import groq as client
from util.models import GroqModels
from util.dtypes import WSRequest

from core.model_advice import model_advice_response
from core.dataset_gen import dataset_build_response

# async def example_async_stream(data: Any, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
#     async for chunk in await client.chat.completions.create(
#         model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
#         messages=[{"role": "user", "content": data["text"]}],
#         temperature=1,
#         max_tokens=1024,
#         top_p=1,
#         stream=True,
#         stop=None,
#     ):
#         content = chunk.choices[0].delta.content
#         print(content)
#         await send_handler({"part": content or ""})

async def respond(data: WSRequest, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    if(data.type == "idea_input"):
        await model_advice_response(data, send_handler)
    elif (data.type == "dataset_input"):
        await dataset_build_response(data, send_handler)

