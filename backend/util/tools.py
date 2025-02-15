from util.dtypes import Tool, FunctionDetails, FunctionParameters


PICK_MODEL_TOOL = Tool(
    type="function",
    function=FunctionDetails(
        name="pick_model",
        description="Present the user with options to pick a model to fine tune.",
        parameters=FunctionParameters(
            properties={},
            required=None
        )
    )
).model_dump()