from fastapi import APIRouter
from kitchen.services.inventory_manager import add_stock , get_inventory , update_stock
from pydantic import BaseModel

class StockInput(BaseModel):
    item:str
    quantity:int
    unit:str

class StockResponse(BaseModel):
    item:str
    quantity:int
    unit:str
    status:str

class ApiResponse(BaseModel):
    status:str
    data:StockResponse
    
router=APIRouter()

@router.get("/inventory",response_model=ApiResponse)
def view_inventory():
    data=get_inventory()
    return{
        "status":"success",
        "data":data
    }
@router.put("/stock/{item}",response_model=ApiResponse)
def update_inventory(data:StockInput):
    result=update_stock(data.item,data.quantity)
    return{
        "status":"success",
        "data":result
    }
@router.post("/stock",response_model=ApiResponse)
def add_inventory(data:StockInput):
    result=add_stock(data.item,data.quantity,data.unit)
    return{
        "status":"success",
        "data":result
    }