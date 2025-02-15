import json
from datetime import datetime

def make_json_serializable(data):
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, datetime):
        return data.isoformat()
    return data