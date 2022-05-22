from enum import IntEnum
from http import HTTPStatus


def get_response(err: bool, msg: str, data: 'dict[str, any]' = None, status_code: int = HTTPStatus.ACCEPTED):
    return {
        "error": err,
        "message": msg,
        "data": data
    }, status_code

def get_response_with_single_payload(status_code: int, data: 'dict[str, any]' = None):
    return data, status_code
