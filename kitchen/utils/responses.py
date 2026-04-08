from typing import Any


def success_response(data: Any = None, message: str = "Success") -> dict:
    """Standard success response for all routes"""
    response = {
        "success": True,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return response


def error_response(message: str = "An error occurred") -> dict:
    """Standard error response (used in global exception handler)"""
    return {
        "success": False,
        "message": message,
    }
