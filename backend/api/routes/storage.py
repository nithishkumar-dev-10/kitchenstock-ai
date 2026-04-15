from fastapi import APIRouter, HTTPException
from kitchen.services.storage_advisor import get_storage_advice, get_all_storage_advice
from kitchen.services.data_loader import load_inventory
from kitchen.schemas.response_schema import APIResponse
from kitchen.utils.responses import success_response

router = APIRouter()


@router.get("/storage", response_model=APIResponse)
async def get_storage_for_all():
    """Get storage advice for all inventory items."""
    inventory = load_inventory()
    result = get_all_storage_advice(inventory)
    return success_response(data=result)


@router.get("/storage/{item_name}", response_model=APIResponse)
async def get_storage_for_item(item_name: str):
    """Get storage advice for a specific item."""
    result = get_storage_advice(item_name)
    return success_response(data=result)