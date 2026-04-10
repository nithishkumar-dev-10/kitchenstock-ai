from fastapi import APIRouter, HTTPException
from kitchen.services.consumption_analyzer import ConsumptionAnalyzer
from kitchen.schemas.response_schema import APIResponse
from kitchen.utils.responses import success_response
from pydantic import BaseModel, Field

router = APIRouter()


class DishLogInput(BaseModel):
    dish_name: str = Field(..., min_length=1, example="idli")
    servings: int = Field(..., ge=1, example=2)
    date: str = Field(..., example="2026-04-10")


@router.post("/consumption/log", response_model=APIResponse)
async def log_dish(data: DishLogInput):
    try:
        analyzer = ConsumptionAnalyzer()
        result = analyzer.log_dish(data.dish_name, data.servings, data.date)
        return success_response(data=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/consumption/daily", response_model=APIResponse)
async def get_daily_usage():
    try:
        analyzer = ConsumptionAnalyzer()
        result = analyzer.get_daily_usage()
        return success_response(data=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consumption/estimate", response_model=APIResponse)
async def estimate_missing(from_date: str, to_date: str):
    try:
        analyzer = ConsumptionAnalyzer()
        result = analyzer.estimate_missing_days(from_date, to_date)
        return success_response(data=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))