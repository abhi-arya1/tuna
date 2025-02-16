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

#### GET PROMPT/PLAN FOR DATASET SCRAPING

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
            
            THIS IS THE PROMPT THAT THE SCRAPER RECIEVES. YOUR QUESTION SHOULD BE OPTIMIZED TO THIS: 
                You are a model in a dataset generation pipeline. 
                Your job is to use the user query to search for relevant sources that can
                supplement the dataset. Explain the sources you provide in very brief detail,
                All sources will then be used to turn into an input/output dataset for a text-generation
                model or agent. 
                You will be given a query from your friend in the pipeline that will guide you towards the 
                relevant URLs required.
                You should SPECIFICALLY look for sources that can be used to train a text-generation model.
                Rank your sources based on the quality of code/output examples and details they can provide.
                HIGHEST QUALITY SOURCES/CITATIONS SHOULD COME FIRST.
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


#### GET TEXT REPLY

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


#### BUILD DATASET FILE

async def build_dataset(
    sources: list,
    data: str, 
    planner_prompt: str, 
    scrape_detail: dict, 
    send_handler: Callable[[dict, Literal["text"]], None]
) -> None:
    final_prompt = ""
    async for chunk in await client.chat.completions.create(
        model=GroqModels.QWEN_2_5_CODER_32B.value,
        messages=[{
            "role": "system",
            "content": """
            You are a dataset generation code generation agent. Your job is to create inputs and outputs
            in the JSONL format given some background information. You will be given the user's initial query 
            to generate this dataset, as well as the details from an accurate web-scraper that has 
            the actual formatted model response in `requested_item` and the details of the response for your information in `item_detail`.
            Given these details, generate the code for the file in the following format.

            { "input": "<A realistic query that the user would provide to the model>", "output": "<The response/requested_item>" }

            You MUST provide nothing at all but the code here, and YOU MUST ALWAYS INCLUDE AT LEAST 20 ENTRIES. Good luck! 
            """
        }, {
            "role": "user",
            "content": f"""
            My initial query {data} was used to plan the dataset generation request. 
            The plan was {planner_prompt}. The web-scraper provided the following details about 
            accurate input-output based on this: 
            {scrape_detail}
            Now, its your job to generate the dataset file in JSONL format.
            """
        }],
        temperature=1,
        max_tokens=4092,
        top_p=1,
        stream=True,
        stop=None,
    ):
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content.replace("```", "").replace("json", "").replace("```", "").replace("jsonl", "")
            final_prompt += content
        else:
            continue

        await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": f"{content if final_prompt else get_log_format(content)}" or "",
            "sources": sources,
            "complete": False
        })
    
    await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": "\n",
            "sources": sources,
            "complete": False
        })
    await send_handler({
            "text": "",
            "type": "ds_generation",
            "dataset": [],
            "log": get_log_format(f"Dataset file generated successfully. Time to train", tuna_msg=True),
            "sources": sources,
            "complete": False
        })
    
    # print(final_prompt)
    with open("data/dataset.jsonl", "w") as f:
        f.write(final_prompt)
    return final_prompt


#### FINAL DELIVERY

async def dataset_build_response(data: WSRequest, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    usrprompt = data.text
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
    
    async with websockets.connect("ws://localhost:8080/ws") as websocket:
        url = response.citations[0]
        if response.citations[0].endswith(".pdf"):
            url = response.citations[1]
        if "github" in response.citations[0]:
            url = response.citations[1]
        
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
            # print("Recieved data: ", message)
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


    await build_dataset(sources, usrprompt, planned_prompt, response, send_handler)

    


    
