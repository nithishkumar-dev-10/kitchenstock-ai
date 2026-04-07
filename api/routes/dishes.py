from fastapi import APIRouter, HTTPException
from kitchen.services.dish_engine import cook_dish
from kitchen.services.dish_checker import check_ingredients
from kitchen.schemas.dish_schema import DishInput, DishResponse, DishCheckInput

router = APIRouter()

@router.post("/dishes/check")
def check_dish(data: DishCheckInput):
    result = check_ingredients(data.dish_name, data.servings)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return {"status": "success", "data": result}


@router.post("/dishes/cook", response_model=DishResponse)
def cook(data: DishInput):
    result = cook_dish(data.dish_name, data.servings)
    
    if "error" in result or result.get("status") == "failed":
        raise HTTPException(
            status_code=400,
            detail=result.get("error") or result.get("message")
        )
    
    return {"status": "success", "updated": result}