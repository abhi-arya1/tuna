from enum import Enum

class GroqModels(Enum):
    LLAMA_3_3_70B_VERSATILE="llama-3.3-70b-versatile"
    DEEPSEEK_R1_DISTILL_LLAMA_70B="deepseek-r1-distill-llama-70b"
    QWEN_2_5_CODER_32B="qwen-2.5-coder-32b"
    LLAMA_3_1_8B_INSTANT="llama-3.1-8b-instant"


class PerplexityModel(Enum):
    SONAR="sonar"
    SONAR_PRO="sonar-pro"
    SONAR_REASONING="sonar-reasoning"
    SONAR_REASONING_PRO="sonar-reasoning-pro"
