import json
from kitchen.services.dish_checker import check_ingredients, load_dishes, load_inventory
from kitchen.utils.exceptions import ItemNotFoundError, InsufficientStockError, DataLoadError


def save_inventory(inventory: dict) -> None:
    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)


def cook_dish(dish_name: str, servings: int) -> dict:
    # This will raise ItemNotFoundError or InvalidInputError if something is wrong
    check_result = check_ingredients(dish_name, servings)

    if not check_result.get("can_cook"):
        missing = [
            i["item"] for i in check_result["ingredients"] if not i["enough"]
        ]
        raise InsufficientStockError(
            f"Not enough ingredients to cook '{dish_name}'. Missing: {', '.join(missing)}"
        )

    dishes = load_dishes()
    inventory = load_inventory()

    ingredients = dishes[dish_name]
    updated_items = []

    for item, qty in ingredients.items():
        required = qty * servings

        if item not in inventory:
            raise ItemNotFoundError(f"'{item}' not found in inventory")

        inventory[item]["quantity"] -= required

        if inventory[item]["quantity"] < 0:
            inventory[item]["quantity"] = 0

        updated_items.append({
            "item": item,
            "quantity": inventory[item]["quantity"],
            "unit": inventory[item].get("unit", "")
        })

    save_inventory(inventory)

    return {
        "dish_name": dish_name,
        "servings": servings,
        "updated_inventory": updated_items
    }