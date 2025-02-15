from typing import AsyncIterator, Optional
from util.dtypes import PerplexityStreamingResponse
import httpx, json
from pydantic import ValidationError
from util.models import PerplexityModel
from os import getenv


async def stream_pplx_response(
    messages: list[dict]
) -> AsyncIterator[PerplexityStreamingResponse]:
    payload = {
        "model": "sonar",
        "messages": messages,
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
                        yield parsed_response
                    except (json.JSONDecodeError, ValidationError) as e:
                        print(f"Error parsing response: {e}")