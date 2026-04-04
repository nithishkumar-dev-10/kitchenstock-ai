from fastapi import APIRouter
from pydantic import BaseModel
from kitchen.services.dish_engine import cook_dish
from typing import List,Dict
from fastapi import HTTPException

router=APIRouter()

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


@router.put("/cook",response_model=DishResponse)
def cook(data:DishInput):
    result=cook_dish(data.dish_name,data.servings)
    if "error" in result or result.get("status") == "failed":
        raise HTTPException(
            status_code=400,
            detail=result.get("error") or result.get("message")
        )
    return{
        "status":"success",
        "updated":result
    }