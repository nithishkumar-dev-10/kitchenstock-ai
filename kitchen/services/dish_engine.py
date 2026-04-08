from kitchen.services.data_loader import load_dishes, load_inventory, save_inventory
from kitchen.services.dish_checker import check_ingredients
from kitchen.utils.exceptions import ItemNotFoundError, InsufficientStockError


def cook_dish(dish_name: str, servings: int) -> dict:
    # Raises ItemNotFoundError or InvalidInputError if something is wrong
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

        # Clamp to 0 — prevent negative stock
        if inventory[item]["quantity"] < 0:
            inventory[item]["quantity"] = 0

        updated_items.append({
            "item": item,
            "quantity": inventory[item]["quantity"],
            "unit": inventory[item].get("unit", "")  # Safe: default empty string
        })

    save_inventory(inventory)

    return {
        "dish_name": dish_name,
        "servings": servings,
        "updated_inventory": updated_items
    }
