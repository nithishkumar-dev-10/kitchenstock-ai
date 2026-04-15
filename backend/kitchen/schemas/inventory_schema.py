from pydantic import BaseModel, Field
from typing import Dict, Optional


class InventoryItem(BaseModel):
    quantity: float = Field(..., gt=0, example=2.5)
    unit: str = Field(..., min_length=1, example="kg")
    expiry_date: Optional[str] = Field(None, example="2026-05-10")

class InventoryResponse(BaseModel):
    status: str
    data: Dict[str, InventoryItem]

class StockInput(BaseModel):
    item: str = Field(..., min_length=1, example="rice")
    quantity: float = Field(..., gt=0, example=2.5)
    unit: str = Field(..., min_length=1, example="kg")
    expiry_date: Optional[str] = Field(None, example="2026-05-10")

class StockResponse(BaseModel):
    item: str
    quantity: float
    unit: str
    expiry_date: Optional[str] = None
    status: str

class APIResponse(BaseModel):
    status: str
    data: StockResponse

class UpdateStock(BaseModel):
    quantity: float = Field(..., gt=0, example=1.0)