from fastapi import APIRouter, HTTPException
from kitchen.services.alert_system import check_alerts
from kitchen.utils.exceptions import DataLoadError, NoDataAvailableError
from kitchen.utils.responses import success_response
from kitchen.schemas.alert_schema import APIResponse

router = APIRouter()


@router.get("/alerts", response_model=APIResponse)
def get_alerts():
    try:
        result = check_alerts()
        return success_response(data=result)

    except NoDataAvailableError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))