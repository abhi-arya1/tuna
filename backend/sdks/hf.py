from huggingface_hub import HfApi
from util.dtypes import TASK_TEXT_GENERATION, TASK_TEXT_TO_IMAGE
from dataclasses import asdict

api = HfApi()


def get_models(): 
    return list(map(lambda x: asdict(x), api.list_models(
        task=TASK_TEXT_GENERATION,
        sort="downloads",
        library="pytorch",
        limit=10
    )))

