from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel

### AI TOOL CALL SDK (OPENAI STYLE)

class FunctionParameters(BaseModel):
    type: Literal["object"] = "object"
    properties: Dict[str, Any]
    required: Optional[List[str]] = None

class FunctionDetails(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters

class Tool(BaseModel):
    type: Literal["function"] = "function"
    function: FunctionDetails

class ToolsList(BaseModel):
    tools: List[Tool]


### HUGGINGFACE MODEL REQUEST TYPES

TASK_TEXT_TO_IMAGE = "text-to-image"
TASK_TEXT_GENERATION = "text-generation"