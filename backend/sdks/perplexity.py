from typing import Optional, Callable, Literal
from util.dtypes import PerplexityStreamingResponse
import httpx, json
from pydantic import ValidationError
from util.models import PerplexityModel
from os import getenv
from util.helpers import get_log_format


async def stream_pplx_response(
    prompt: str,
    send_handler: Optional[Callable[[dict, Literal["text"]], None]] = None,
):
    final_req = ""
    payload = {
        "model": PerplexityModel.SONAR_PRO.value,
        "messages": [
            {
                "role": "system",
                "content": """
                You are a model in a dataset generation pipeline. 
                Your job is to use the user query to search for relevant sources that can
                supplement the dataset. Explain the sources you provide in very brief detail, 
                and ALWAYS include a relevant huggingface dataset that can help train the model. 
                All sources will then be used to turn into an input/output dataset for a text-generation
                model or agent. 
                You will be given a query from your friend in the pipeline that will guide you towards the 
                relevant URLs required.
                You should SPECIFICALLY look for sources that can be used to train a text-generation model.
                """,
            }, 
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 256,
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
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", "https://api.perplexity.ai/chat/completions", json=payload, headers=headers) as response:
            async for line in response.aiter_lines():
                print(line)
                if not line: 
                    continue
                if line.startswith("data: "):
                    try:
                        json_data = json.loads(line[6:])
                        parsed_response = PerplexityStreamingResponse.model_validate(json_data)
                        content = parsed_response.choices[0].delta.content
                        await send_handler({
                            "text": "",
                            "type": "ds_generation",
                            "dataset": [],
                            "log": (get_log_format(content) if not final_req else content) or "",
                            "sources": parsed_response.citations,
                            "complete": False
                        })
                        if content:
                            final_req += content
                    except (json.JSONDecodeError, ValidationError) as e:
                        print(f"Error parsing response: {e}")

    await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": "\n",
            "sources": [],
            "complete": False
        })