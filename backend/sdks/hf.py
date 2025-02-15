from huggingface_hub import HfApi
from util.dtypes import TASK_TEXT_GENERATION
from dataclasses import asdict
from util.helpers import make_json_serializable

api = HfApi()
clean_models = lambda models: list(map(lambda x: make_json_serializable(asdict(x)), models))


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
