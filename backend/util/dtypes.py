from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel
from enum import Enum 

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

### ENUMS FOR CHAT TYPES (TRAINING)

class ChatTypes(Enum):
    USER_INPUT="user_input"
    MODEL_ADVICE="model_advice"
    DS_GENERATION="ds_generation"
    TRAIN_INST_SELECTION="train_inst_selection"
    TRAIN_DETAILS="train_details"
    DEPLOYMENT="deployment"
    ERROR="error"


### REQUEST TYPE MODELS 

class WSRequest(BaseModel):
    type: Literal["idea_input", "dataset_input", "model_choice", "train_instance_choice", "deploy"]
    text: Optional[str] = None 
    button: Optional[dict | Any] = None


### RESPONSE TYPE MODELS 

class UserInput(BaseModel):
    text: str 

class ModelAdvice(BaseModel):
    text: str 
    recommendation: str 
    model_list: str 

class DSGeneration(BaseModel):
    text: str 
    dataset: list[dict]
    log: str 
    sources: list[str]

class TrainInstanceSelection(BaseModel):
    text: str 
    instances: list[dict]

class TrainDetails(BaseModel):
    text: str 
    log: str 

class Deployment(BaseModel):
    text: str 
    metadata: dict
