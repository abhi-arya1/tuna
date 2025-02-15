from typing import Optional, Callable, Literal
from util.dtypes import PerplexityStreamingResponse
import httpx, json
from pydantic import ValidationError
from util.models import PerplexityModel
from os import getenv
from util.dtypes import WSRequest
from util.helpers import get_log_format


async def stream_pplx_response(
    data: WSRequest,
    prompt: str,
    send_handler: Optional[Callable[[dict, Literal["text"]], None]] = None,
):
    payload = {
        "model": PerplexityModel.SONAR_PRO.value,
        "messages": [
            {
                "role": "system",
                "content": "",
            }, 
            {

            }
        ],
        "max_tokens": 123,
        "temperature": 0.2,
        "top_p": 0.9,
        "search_domain_filter": None,
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": None,
        "top_k": 0,
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 1,
        "response_format": None
    }

    headers = {
        "Authorization": f"Bearer {getenv("PPLX_API_KEY")}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", "https://api.perplexity.ai/chat/completions", json=payload, headers=headers) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    try:
                        json_data = json.loads(line[6:])
                        parsed_response = PerplexityStreamingResponse.model_validate(json_data)
                        await send_handler({
                            "text": "",
                            "type": "ds_generation",
                            "dataset": [],
                            "log": get_log_format(parsed_response.choices[0].delta.content),
                            "sources": parsed_response.citations,
                            "complete": False
                        })
                    except (json.JSONDecodeError, ValidationError) as e:
                        print(f"Error parsing response: {e}")