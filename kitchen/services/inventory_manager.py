from kitchen.services.data_loader import load_inventory, save_inventory
from kitchen.utils.exceptions import ItemNotFoundError, InvalidInputError


def get_inventory() -> dict:
    return load_inventory()


def add_stock(item: str, quantity: float, unit: str) -> dict:
    if quantity <= 0:
        raise InvalidInputError("Quantity must be greater than 0")

    inventory = load_inventory()

    if item in inventory:
        inventory[item]["quantity"] += quantity
        status = "updated"
    else:
        inventory[item] = {"quantity": quantity, "unit": unit}
        status = "added"

    save_inventory(inventory)

    return {
        "item": item,
        "quantity": inventory[item]["quantity"],
        "unit": inventory[item]["unit"],
        "status": status
    }


def update_stock(item: str, quantity: float) -> dict:
    if quantity <= 0:
        raise InvalidInputError("Quantity must be greater than 0")

    inventory = load_inventory()

    if item not in inventory:
        raise ItemNotFoundError(f"Item '{item}' not found in inventory")

    inventory[item]["quantity"] = quantity
    save_inventory(inventory)

    return {
        "item": item,
        "quantity": quantity,
        "unit": inventory[item]["unit"],
        "status": "updated"
    }


def delete_stock(item: str) -> dict:
    inventory = load_inventory()

    if item not in inventory:
        raise ItemNotFoundError(f"Item '{item}' not found in inventory")

    del inventory[item]
    save_inventory(inventory)

    return {"item": item, "status": "deleted"}
