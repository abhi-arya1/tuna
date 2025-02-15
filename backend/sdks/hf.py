from huggingface_hub import HfApi
from util.dtypes import TASK_TEXT_GENERATION
from dataclasses import asdict

api = HfApi()
clean_models = lambda models: list(map(lambda x: asdict(x), models))


def get_models(): 
    return clean_models(api.list_models(
            task=TASK_TEXT_GENERATION,
            sort="trending_score",
            library="pytorch",
            limit=10
        ))


def search_models(search_term: str):
    return clean_models(api.list_models(
            search=search_term,
            task=TASK_TEXT_GENERATION,
            sort="trending_score",
            library="pytorch",
            limit=7
        ))
