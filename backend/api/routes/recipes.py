from fastapi import APIRouter, HTTPException
from kitchen.services.recipe_suggester import suggest_recipes
from kitchen.schemas.response_schema import APIResponse
from kitchen.schemas.recipe_schema import RecipeSuggestInput
from kitchen.utils.exceptions import InvalidInputError, NoDataAvailableError, DataLoadError
from kitchen.utils.responses import success_response

router = APIRouter()


@router.post("/recipes/suggest", response_model=APIResponse)
async def get_recipes(data: RecipeSuggestInput):
    try:
        result = suggest_recipes(data.max_missing)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=e.message)

    except NoDataAvailableError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)
