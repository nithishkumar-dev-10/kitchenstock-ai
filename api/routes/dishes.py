from fastapi import APIRouter, HTTPException
from kitchen.services.dish_checker import check_ingredients
from kitchen.services.dish_engine import cook_dish
from kitchen.schemas.response_schema import APIResponse
from kitchen.schemas.dish_schema import DishRequest
from kitchen.utils.exceptions import (
    InvalidInputError,
    ItemNotFoundError,
    InsufficientStockError,
    DataLoadError,
)
from kitchen.utils.responses import success_response

router = APIRouter()


@router.post("/dishes/check", response_model=APIResponse)
async def check_dish(data: DishRequest):
    try:
        result = check_ingredients(data.dish_name, data.servings)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=e.message)

    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.post("/dishes/cook", response_model=APIResponse)
async def cook(data: DishRequest):
    try:
        result = cook_dish(data.dish_name, data.servings)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=e.message)

    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except InsufficientStockError as e:
        raise HTTPException(status_code=400, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)
