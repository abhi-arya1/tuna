from typing import Callable, Literal
from sdks.groqapi import groq as client, syncgroq
from util.models import GroqModels
from util.dtypes import WSRequest, ModelAdvice, UserInput
from sdks.hf import get_models
from util.dtypes import Tool, FunctionDetails, FunctionParameters
from groq import BadRequestError
from json import loads


async def model_advice_response(data: WSRequest, send_handler: Callable[[dict, Literal["text"]], None]) -> None:
    tool_call_id = "call_d234"
    models = get_models()
    model_list = "\n".join(model["id"] for model in models)
    recommendation = models[0]["id"]

    try: 
        completion = syncgroq.chat.completions.create(
            model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
            messages=[{
                "role": "system",
                "content": "You are a model picking agent. Based on a user query, your job is to pick a model exactly by name from the list of models provided that best fits the user's needs."
            }, {
                "role": "user",
                "content": data.text
            }, {
                "role": "assistant",
                "type": "function",
                "function": {
                    "name": "get_models",
                }
            }, {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": "get_models",
                "content": f"Here are the available models that you MUST choose from:\n{model_list}"
            }],
            tools=[
                Tool(
                    type="function",
                    function=FunctionDetails(
                        name="pick_model",
                        description="Provide the exact name of the model you want to fine tune.",
                        parameters=FunctionParameters(
                            properties={"model": {"type": "string"}},
                            required=["model"]
                        )
                    )
                ).model_dump()
            ]
        )
        response = completion.choices[0].message
        tool_calls = response.tool_calls
        for tool_call in tool_calls:
            function_args = loads(tool_call.function.arguments)
            recommendation = function_args.get("model", recommendation)
            break
    except BadRequestError as e:
        pass

    chosen_model = next(model for model in models if model["id"] == recommendation)

    async for chunk in await client.chat.completions.create(
        model=GroqModels.LLAMA_3_3_70B_VERSATILE.value,
        messages=[{
            "role": "system",
            "content": """
            You are an AI expert who is assisting in selecting an AI model for a user. 
            Based on a user query, your job is to recommend a model from the list of models 
            provided that best fits the user's needs. Once recommended, you must provide a 
            brief explanation of your choice, NO MORE THAN TWO SENTENCES KEPT BRIEF AND CONCISE, 
            as to why this may help the user's use case. 
            DO NOT USE ANY MARKDOWN SYNTAX IN YOUR RESPONSE. 
            RESPOND WITH RAW TEXT ONLY. NO MARKDOWN."""
        }, {
            "role": "user",
            "content": data.text
        }, {
            "role": "assistant",
            "content": recommendation
        }, {
            "role": "user",
            "content": "In exactly two sentences, breifly describe why you chose this model."
        }],
        temperature=1,
        max_completion_tokens=512,
        top_p=1,
        stream=True,
        stop=None,
    ):
        content = chunk.choices[0].delta.content
        await send_handler({
            "text": content or "",
            "recommendation": chosen_model,
            "model_list": model_list
        })