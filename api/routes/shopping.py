from fastapi import APIRouter,HTTPException
from kitchen.services.shopping_list import generate_shopping_list
from kitchen.schemas.shopping_schema import ShoppingData,ShoppingResponse

router=APIRouter()



@router.get("/shopping-list",response_model=ShoppingResponse)
def shopping():
    result=generate_shopping_list()

    if not result:
        raise HTTPException(status_code=404, detail="Unable to genarate shopping list")
    return{
        "status":"success",
        "shopping_list":result


    }

