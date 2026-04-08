from typing import Any


def success_response(data: Any = None, message: str = None) -> dict:
    """Standard success response for all routes"""
    response = {"status": "success"}

    if message:
        response["message"] = message

    if data is not None:
        response["data"] = data

    return response