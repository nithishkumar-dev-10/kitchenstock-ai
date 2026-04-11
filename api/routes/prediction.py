from fastapi import APIRouter, HTTPException
from kitchen.services.prediction_engine import predict_runout
from kitchen.schemas.response_schema import APIResponse
from kitchen.utils.exceptions import NoDataAvailableError, DataLoadError
from kitchen.utils.responses import success_response

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.get("/runout", response_model=APIResponse)
async def get_runout_predictions():
    try:
        result = predict_runout()
        return success_response(data=result)

    except NoDataAvailableError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)