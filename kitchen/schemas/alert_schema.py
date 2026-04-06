from pydantic import BaseModel
from typing import List


class AlertData(BaseModel):
    low_stock: List[str]
    out_of_stock: List[str]
    message: str


class AlertResponse(BaseModel):
    status: str
    alerts: AlertData