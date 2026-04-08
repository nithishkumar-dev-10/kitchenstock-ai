from fastapi import APIRouter, HTTPException
from kitchen.services.shopping_list import generate_shopping_list
from kitchen.schemas.response_schema import APIResponse
from kitchen.utils.exceptions import DataLoadError, NoDataAvailableError
from kitchen.utils.responses import success_response

router = APIRouter()


@router.get("/shopping", response_model=APIResponse)
async def get_shopping_list():
    try:
        result = generate_shopping_list()
        return success_response(data=result)

    except NoDataAvailableError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)
