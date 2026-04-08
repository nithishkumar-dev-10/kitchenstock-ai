from fastapi import APIRouter, HTTPException
from kitchen.services.inventory_manager import add_stock, get_inventory, update_stock
from kitchen.schemas.inventory_schema import InventoryResponse, APIResponse, UpdateStock, StockInput
from kitchen.utils.exceptions import (
    InvalidInputError,
    ItemNotFoundError,
    DataLoadError
)
from kitchen.utils.responses import success_response

router = APIRouter()


@router.get("/inventory", response_model=InventoryResponse)
def view_inventory():
    try:
        data = get_inventory()
        return success_response(data=data)

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/inventory", response_model=APIResponse)
def add_inventory(data: StockInput):
    try:
        result = add_stock(data.item, data.quantity, data.unit)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/inventory/{item_name}", response_model=APIResponse)
def update_inventory(item_name: str, data: UpdateStock):
    try:
        result = update_stock(item_name, data.quantity)
        return success_response(data=result)

    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ItemNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except DataLoadError as e:
        raise HTTPException(status_code=500, detail=str(e))