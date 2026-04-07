from pydantic import BaseModel, Field
from typing import Dict

class InventoryItem(BaseModel):
    quantity: float = Field(..., gt=0, example=2.5)
    unit: str = Field(..., min_length=1, example="kg")

class InventoryResponse(BaseModel):
    status: str
    data: Dict[str, InventoryItem]

class StockInput(BaseModel):
    item: str = Field(..., min_length=1, example="rice")
    quantity: float = Field(..., gt=0, example=2.5)
    unit: str = Field(..., min_length=1, example="kg")

class StockResponse(BaseModel):
    item: str
    quantity: float
    unit: str
    status: str

class APIResponse(BaseModel):
    status: str
    data: StockResponse

class UpdateStock(BaseModel):
    quantity: float = Field(..., gt=0, example=1.0)