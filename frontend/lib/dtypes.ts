

type User = {
    id: string;
    name: string;
    email: string;
    avatar_url: string;
    projects: string[];
}

type Project = {
    id: string; 
    created_at: string; 
    creator_id: string; 
    name: string; 
    chat_history: any[];
    metadata: any;
}

type HFModel = {
    id: string;
    author: null | string;
    sha: null | string;
    created_at: string;
    last_modified: null | string;
    private: boolean;
    disabled: null | boolean;
    downloads: number;
    downloads_all_time: null | number;
    gated: null | boolean;
    gguf: null | boolean;
    inference: null | boolean;
    likes: number;
    library_name: string;
    tags: string[];
    pipeline_tag: string;
    mask_token: null | string;
    card_data: null | object;
    widget_data: null | object;
    model_index: null | object;
    config: null | object;
    transformers_info: null | object;
    trending_score: null | number;
    siblings: null | object[];
    spaces: null | object;
    safetensors: null | boolean;
    security_repo_status: null | string;
  };

enum ProjectMakeStatus {
    USER_INPUT="user_input",
    MODEL_ADVICE="model_advice",
    DS_INPUT="dataset_input",
    DS_GENERATION="ds_generation",
    DS_VISUALIZATION="ds_visualization",
    TRAIN_INST_SELECTION="train_inst_selection",
    TRAIN_DETAILS="train_details",
    DEPLOYMENT="deployment",
    ERROR="error"
}

type EC2Instance = {
    id: string;
    aws_id: string;
    provider: string;
    platform: string;
    gpu: string;
    memory_gb: number;
    storage_gb: number;
    vcpus: number;
}

const EC2_P5: EC2Instance = {
    id: "ec2_p5",
    aws_id: "p5.48xlarge",
    provider: "NVIDIA",
    platform: "AWS",
    gpu: "H100",
    memory_gb: 2048,
    storage_gb: 30400,
    vcpus: 192,
}

const EC2_G4DN: EC2Instance = {
    id: "ec2_g4dn",
    aws_id: "g4dn.8xlarge",
    provider: "NVIDIA",
    platform: "AWS",
    gpu: "T4",
    memory_gb: 128,
    storage_gb: 900,
    vcpus: 32,
}

// class UserInput(BaseModel):
//     text: str 

// class ModelAdvice(BaseModel):
//     text: str 
//     recommendation: str 
//     model_list: str 

// class DSGeneration(BaseModel):
//     text: str 
//     dataset: list[dict]
//     log: str 
//     sources: list[str]

// class TrainInstanceSelection(BaseModel):
//     text: str 
//     instances: list[dict]

// class TrainDetails(BaseModel):
//     text: str 
//     log: str 

// class Deployment(BaseModel):
//     text: str 
//     metadata: dict

export { 
    ProjectMakeStatus,
    EC2_P5,
    EC2_G4DN
}

export type {
    User,
    Project,
    HFModel,
    EC2Instance
};