import json


def DECODE_FIELDS_FILE(json_str: str) -> dict:
    return json.loads(json_str)
