from fastapi import APIRouter, HTTPException
from kitchen.services.dish_checker import check_ingredients
from kitchen.services.dish_engine import cook_dish
from kitchen.schemas.dish_schema import DishRequest, APIResponse
from kitchen.utils.exceptions import InvalidInputError,ItemNotFoundError,InsufficientStockError,DataLoadError

from kitchen.utils.responses import success_response

router = APIRouter()



@router.post("/dishes/check", response_model=APIResponse)
def check_dish(data: DishRequest):
    try:
        result = check_ingredients(data.dish_name, data.servings)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/dishes/cook", response_model=APIResponse)
def cook(data: DishRequest):
    try:
        result = cook_dish(data.dish_name, data.servings)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))