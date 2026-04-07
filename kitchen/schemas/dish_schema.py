from pydantic import BaseModel, Field
from typing import List

class DishInput(BaseModel):
    dish_name: str = Field(..., min_length=1, example="biryani")
    servings: int = Field(..., ge=1, example=2)

class DishCheckInput(BaseModel):
    dish_name: str = Field(..., min_length=1, example="biryani")
    servings: int = Field(..., ge=1, example=2)

class InventorySnapshot(BaseModel):
    item: str
    quantity: float
    unit: str

class DishData(BaseModel):
    dish_name: str
    servings: int
    updated_inventory: List[InventorySnapshot]

class DishResponse(BaseModel):
    status: str
    updated: DishData