from fastapi import APIRouter
from kitchen.schemas.alert_schema import AlertResponse
from kitchen.services.alert_system import check_alerts

router=APIRouter()



@router.get("/alert",response_model=AlertResponse)
def alert_sys():
    result=check_alerts()
    return{
        "status":"success",
        "alerts":result

    }

