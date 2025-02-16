from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from enum import Enum 
from datetime import datetime

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
    DS_VISUALIZATION="ds_visualization"
    TRAIN_INST_SELECTION="train_inst_selection"
    TRAIN_DETAILS="train_details"
    DEPLOYMENT="deployment"
    ERROR="error"


### REQUEST TYPE MODELS 

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = True

class ChatCompletionResponse(BaseModel):
    id: str = Field(default="chatcmpl-default")
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[dict]
    usage: dict
    

class WSRequest(BaseModel):
    type: Literal["idea_input", "dataset_input", "model_choice", "train_instance_choice", "train", "deploy"]
    text: Optional[str] = None 
    button: Optional[dict | Any] = None


### RESPONSE TYPE MODELS 

class UserInput(BaseModel):
    type: str
    text: str 

class ModelAdvice(BaseModel):
    type: str
    text: str 
    recommendation: str 
    model_list: str 

class DSGeneration(BaseModel):
    type: str
    text: str 
    dataset: list[dict]
    log: str 
    sources: list[str]
    complete: bool = False

class TrainInstanceSelection(BaseModel):
    type: str
    text: str 
    instances: list[dict]

class TrainDetails(BaseModel):
    type: str
    text: str 
    log: str 
    complete: bool = False

class Deployment(BaseModel):
    type: str
    text: str 
    metadata: dict


### PERPLEXITY STREAM TYPES 

class UsageStats(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class MessageContent(BaseModel):
    role: str
    content: str

class DeltaContent(BaseModel):
    role: Optional[str] = None
    content: Optional[str] = None

class Choice(BaseModel):
    index: int
    finish_reason: Optional[str] = None
    message: MessageContent
    delta: DeltaContent

class PerplexityStreamingResponse(BaseModel):
    id: str
    model: str
    created: int
    usage: UsageStats
    citations: List[str]
    object: str
    choices: List[Choice]


#### EC2 INSTANCE ROLLOUT SYSTEM