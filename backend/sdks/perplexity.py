import asyncio
import httpx
import json
import re 
from typing import Optional, Callable, Literal
from pydantic import ValidationError
from os import getenv
from util.dtypes import PerplexityStreamingResponse
from util.models import PerplexityModel
from util.helpers import get_log_format
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")
NUMBERED_SECTION_REGEX = re.compile(r"^\d+\.\s")

async def stream_pplx_response(
    prompt: str,
    send_handler: Optional[Callable[[dict, Literal["text"]], None]] = None,
) -> tuple[PerplexityStreamingResponse, list]:
    final_req = ""
    final_response = None
    sources = []

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
                Rank your sources based on the quality of code/output examples and details they can provide.
                HIGHEST QUALITY SOURCES/CITATIONS SHOULD COME FIRST. DO NOT USE GITHUB URLS AS SOURCES IN ANY WAY.
                """,
            }, 
            {"role": "user", "content": prompt}
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
                if not line:
                    continue
                if line.startswith("data: "):
                    try:
                        json_data = json.loads(line[6:])
                        parsed_response = PerplexityStreamingResponse.model_validate(json_data)
                        content = parsed_response.choices[0].delta.content

                        is_new_section = bool(NUMBERED_SECTION_REGEX.match(content)) if content else False

                        await send_handler({
                            "text": "",
                            "type": "ds_generation",
                            "dataset": [],
                            "log": (get_log_format(content) if is_new_section else content) or "",
                            "sources": parsed_response.citations,
                            "complete": False
                        })

                        if content:
                            final_req += content
                        if parsed_response.citations:
                            sources = parsed_response.citations
                        final_response = parsed_response

                    except (json.JSONDecodeError, ValidationError) as e:
                        print(f"Error parsing response: {e}")

    await send_handler({
        "text": "",
        "type": "ds_generation",
        "dataset": [],
        "log": "\n",
        "sources": sources,
        "complete": False
    })

    return final_response, sources
