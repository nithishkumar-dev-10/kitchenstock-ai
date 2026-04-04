from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from kitchen.services.alert_system import check_alerts

router=APIRouter()

class AlertData(BaseModel):
    low_stock:List[str]
    out_of_stock:List[str]
    message:str
    

class AlertResponse(BaseModel):
    status:str
    alerts:AlertData

@router.get("/alert",response_model=AlertResponse)
def alert_sys():
    result=check_alerts()
    return{
        "status":"success",
        "alerts":result

    }

