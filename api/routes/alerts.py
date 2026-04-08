from fastapi import APIRouter, HTTPException
from kitchen.services.alert_system import check_alerts
from kitchen.utils.exceptions import DataLoadError, NoDataAvailableError
from kitchen.utils.responses import success_response
from kitchen.schemas.response_schema import APIResponse

router = APIRouter()


@router.get("/alerts", response_model=APIResponse)
async def get_alerts():
    try:
        result = check_alerts()
        return success_response(data=result)

    except NoDataAvailableError as e:
        raise HTTPException(status_code=404, detail=e.message)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=e.message)
