from pydantic import BaseModel
from typing import Any, Optional


class APIResponse(BaseModel):
    success: bool
    message: str = "Success"
    data: Optional[Any] = None
