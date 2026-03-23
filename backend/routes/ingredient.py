from fastapi import APIRouter

router = APIRouter(prefix="/ingredient")

inventory = []
@router.post("/")
def add_item(name: str, quantity: int):
    item = {
        "name": name,
        "quantity": quantity
    }
    inventory.append(item)
    return {"msg": "Item added", "data": item}
    
@router.get("/")
def get_items():
    return inventory
