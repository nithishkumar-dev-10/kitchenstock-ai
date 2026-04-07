from pydantic import BaseModel, Field
from typing import List

class AlertData(BaseModel):
    low_stock: List[str] = Field(default_factory=list, example=["rice", "oil"])
    out_of_stock: List[str] = Field(default_factory=list, example=["salt"])
    message: str = Field(..., min_length=1, example="Items need restocking")

class AlertResponse(BaseModel):
    status: str = Field(..., example="success")
    alerts: AlertData