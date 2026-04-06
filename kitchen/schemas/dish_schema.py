from pydantic import BaseModel
from typing import List,Dict


class DishInput(BaseModel):
    dish_name:str
    servings:int

class DishData(BaseModel):
    dish_name:str
    servings:int
    updated_inventory:List[Dict]
class DishResponse(BaseModel):
    status:str
    updated:DishData

