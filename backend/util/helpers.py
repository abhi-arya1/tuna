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


def get_time_for_log(): 
    return datetime.now().strftime("%H:%M:%S")


def get_log_format(msg: str, tuna_msg: bool = False):
    if tuna_msg:
        return f"<<{get_time_for_log()}>> [TUNA] {msg}..."
    else: 
        return f"<<{get_time_for_log()}>> {msg}"
