from huggingface_hub import HfApi, ModelCard
from util.dtypes import TASK_TEXT_GENERATION
from dataclasses import asdict
from util.helpers import make_json_serializable

api = HfApi()
clean_models = lambda models: list(map(lambda x: make_json_serializable(asdict(x)), models))


def get_model(model_id: str):
    card = ModelCard.load(model_id)
    print(card)
    return card


def get_models(): 
    # Sort: possible values are "last_modified", "trending_score",
    # "created_at", "downloads" and "likes".
    return clean_models(api.list_models(
            task=TASK_TEXT_GENERATION,
            sort="trending_score",
            library="pytorch",
            limit=25
        ))


def search_models(search_term: str):
    return clean_models(api.list_models(
            search=search_term,
            task=TASK_TEXT_GENERATION,
            sort="trending_score",
            library="pytorch",
            limit=7
        ))
