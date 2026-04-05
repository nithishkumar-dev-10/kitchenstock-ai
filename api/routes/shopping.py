from fastapi import APIRouter,HTTPException
from pydantic import BaseModel 
from kitchen.services.shopping_list import generate_shopping_list
from typing import List

router=APIRouter()

class ShoppingData(BaseModel):
    low_stock:List[str]
    out_of_stock:List[str]

class ShoppingResponse(BaseModel):
    status:str
    shopping_list:ShoppingData

@router.get("/shopping-list",response_model=ShoppingResponse)
def shopping():
    result=generate_shopping_list()

    if not result:
        raise HTTPException(status_code=404, detail="Unable to genarate shopping list")
    return{
        "status":"success",
        "shopping_list":result


    }

