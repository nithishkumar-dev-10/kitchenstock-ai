from pydantic import BaseModel
from typing import Dict
from typing import Union

class InventoryItem(BaseModel):
    quantity: float
    unit: str

class InventoryResponse(BaseModel):
    status:str
    data:Dict[str, InventoryItem]

class StockInput(BaseModel):
    item:str
    quantity:float
    unit:str

class StockResponse(BaseModel):
    item:str
    quantity:float
    unit:str
    status:str

class APIResponse(BaseModel):
    status:str
    data:StockResponse
    
class UpdateStock(BaseModel):
    quantity:float
