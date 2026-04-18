from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from kitchen.services.storage_advisor import (
    get_storage_advice,
    get_all_storage_advice,
    get_storage_advice_by_name,
)
from kitchen.services.data_loader import load_inventory
from kitchen.schemas.response_schema import APIResponse
from kitchen.utils.responses import success_response

router = APIRouter()


class StorageCheckInput(BaseModel):
    item: str


@router.get("/storage", response_model=APIResponse)
async def get_storage_for_all():
    """Get storage advice for all inventory items."""
    inventory = load_inventory()
    result = get_all_storage_advice(inventory)
    return success_response(data=result)


@router.post("/storage/check")
async def check_storage_for_any_item(body: StorageCheckInput):
    """
    Check storage type for ANY ingredient name.
    Does NOT require the item to be in inventory.
    This powers the Storage Checker feature page.
    """
    if not body.item or not body.item.strip():
        raise HTTPException(status_code=400, detail="Item name cannot be empty")
    try:
        result = get_storage_advice_by_name(body.item)
        return success_response(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/storage/{item_name}", response_model=APIResponse)
async def get_storage_for_item(item_name: str):
    """Get storage advice for a specific inventory item."""
    result = get_storage_advice(item_name)
    return success_response(data=result)
