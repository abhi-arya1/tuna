import asyncio, json, websockets
from typing import Callable, Literal
from util.dtypes import WSRequest
from sdks.groqapi import groq as client, syncgroq
from util.models import GroqModels
from util.helpers import get_log_format
from sdks.perplexity import stream_pplx_response

# class DSGeneration(BaseModel):
#     type: str
#     text: str
#     dataset: list[dict]
#     log: str
#     sources: list[str]

async def get_plan(data: WSRequest, send_handler: Callable) -> str:
    final_prompt = ""

    async for chunk in await client.chat.completions.create(
        model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
        messages=[{
            "role": "system",
            "content": """
            You are a dataset building planner. Your job is to create a question for a semantic web-scraper
            to generate the sources that you can then scrape to build the dataset of choice, based on the user's
            query. DO NOT INCLUDE ANYTHING IN YOUR RESPONSE BEYOND THE QUESTION FOR THE WEB-SCRAPER LLM.
            """
        }, {
            "role": "user",
            "content": data.text
        }],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    ):
        content = chunk.choices[0].delta.content
        if content:
            final_prompt += content

        await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": (get_log_format(content) if not final_prompt else content) or "",
            "sources": [],
            "complete": False
        })

    await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": "\n",
            "sources": [],
            "complete": False
        })
    return final_prompt



async def get_initial_text(data, send_handler):
    async for chunk in await client.chat.completions.create(
        model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
        messages=[{
            "role": "system",
            "content": """
            You are a dataset building response agent. You work very closely with a user that wants to
            create a dataset to fine-tune their AI model. Your job is to provide a VERY BRIEF detail
            into the plan for building the dataset. DO NOT USE ANY MARKDOWN SYNTAX IN YOUR RESPONSE.
            YOUR RESPONSE MUST BE AT MAXIMUM TWO SENTENCES, AND BRIEFLY DESCRIBE THE PLAN IN A HUMAN-READABLE WAY
            FOR BUILDING THE DATASET.
            """
        }, {
            "role": "user",
            "content": data.text
        }],
        temperature=1,
        max_tokens=512,
        top_p=1,
        stream=True,
        stop=None,
    ):
        content = chunk.choices[0].delta.content
        await send_handler({
            "text": content or "",
            "type": "ds_generation",
            "dataset": [],
            "log": "",
            "sources": [],
            "complete": True
        })




async def dataset_build_response(data: WSRequest, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": get_log_format("Planning prompts for dataset generation", tuna_msg=True),
            "sources": [],
            "complete": False
        })

    planned_prompt, _ = await asyncio.gather(
        get_plan(data, send_handler), 
        get_initial_text(data, send_handler)
    )

    await send_handler({
        "text": "",
        "type": "ds_generation",
        "dataset": [],
        "log": get_log_format("Searching for relevant resources", tuna_msg=True),
        "sources": [],
        "complete": False
    })

    response, sources = await stream_pplx_response(planned_prompt, send_handler)
    url = "https://sketchviz.com/graphviz-examples"
    
    async with websockets.connect("ws://localhost:8080/ws") as websocket:
        await websocket.send(json.dumps({
            "url": url,
            "instruction": """
            Please get me code examples of graphviz from this website.
            The code itself should go in requested_item, with the detail 
            of what the code represents in item_detail. Please pick varying 
            examples to make sure that the dataset is diverse.
            """
        }))

        await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": get_log_format("Scraping sources for data", tuna_msg=True),
            "sources": sources,
            "complete": False
        })
        
        async for message in websocket: 
            print("Recieved data: ", message)
            data = json.loads(message)
            if data["complete"] == True: 
                await send_handler({
                    "type": "ds_generation",
                    "text": "",
                    "dataset": [],
                    "sources": sources,
                    "complete": False,
                    "log": get_log_format(f"{data["data"]["examples"]}\n"),
                })
                break 

            log = data["log"]["message"].strip()
            if log == "LLM cache miss - no cached response found":
                log = "Scraped data example successfully. Moving to next."
            await send_handler({
                "type": "ds_generation",
                "text": "",
                "dataset": [],
                "sources": sources,
                "complete": False,
                "log": get_log_format(f"{log}\n"),
            })

        await send_handler({
            "type": "ds_generation",
            "text": "",
            "dataset": [],
            "sources": sources,
            "complete": False,
            "log": get_log_format("Scraping complete. Generating dataset file", tuna_msg=True),
        })

    


    
