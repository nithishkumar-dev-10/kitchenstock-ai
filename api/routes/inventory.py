from fastapi import APIRouter
from kitchen.services.inventory_manager import add_stock , get_inventory , update_stock
from fastapi import HTTPException
from kitchen.schemas.inventory_schema import InventoryResponse,APIResponse,UpdateStock,StockInput


router=APIRouter()

@router.get("/inventory",response_model=InventoryResponse)
def view_inventory():
    data=get_inventory()
    return{
        "status":"success",
        "data":data
    }
@router.put("/stock/{item}",response_model=APIResponse)
def update_inventory(item:str,data:UpdateStock):
    result=update_stock(item,data.quantity)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
        
    
    return{
        "status":"success",
        "data":result
    }
@router.post("/stock",response_model=APIResponse)
def add_inventory(data:StockInput):
    result=add_stock(data.item,data.quantity,data.unit)

    if result is None:
        raise HTTPException(status_code=404,detail="Failed to add item")
    
    return{
        "status":"success",
        "data":result
    }
