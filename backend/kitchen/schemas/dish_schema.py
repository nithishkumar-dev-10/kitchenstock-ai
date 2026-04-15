from pydantic import BaseModel, Field
from typing import List,Any

class DishRequest(BaseModel):
    dish_name: str = Field(..., min_length=1, example="fried_rice")
    servings: int = Field(..., ge=1, example=2)


class InventorySnapshot(BaseModel):
    item: str
    quantity: float
    unit: str

class DishData(BaseModel):
    dish_name: str
    servings: int
    updated_inventory: List[InventorySnapshot]

class APIResponse(BaseModel):
    status: str
    data: Any