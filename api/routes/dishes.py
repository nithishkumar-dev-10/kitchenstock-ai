from fastapi import APIRouter
from kitchen.services.dish_engine import cook_dish
from fastapi import HTTPException
from kitchen.schemas.dish_schema import DishInput,DishResponse

router=APIRouter()




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