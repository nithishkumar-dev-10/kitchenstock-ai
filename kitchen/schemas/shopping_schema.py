from pydantic import BaseModel, Field
from typing import List

class ShoppingData(BaseModel):
    low_stock: List[str] = Field(default_factory=list, example=["rice"])
    out_of_stock: List[str] = Field(default_factory=list, example=["salt"])

class APIResponse(BaseModel):
    status: str = Field(..., example="success")
    shopping_list: ShoppingData