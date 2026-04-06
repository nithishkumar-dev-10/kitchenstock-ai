from typing import List
from pydantic import BaseModel 

class ShoppingData(BaseModel):
    low_stock:List[str]
    out_of_stock:List[str]

class ShoppingResponse(BaseModel):
    status:str
    shopping_list:ShoppingData