from kitchen.services.data_loader import load_dishes, load_inventory
from kitchen.utils.exceptions import ItemNotFoundError, InvalidInputError


def check_ingredients(dish_name: str, servings: int) -> dict:
    if servings <= 0:
        raise InvalidInputError("Servings must be greater than 0")

    dishes = load_dishes()

    if dish_name not in dishes:
        raise ItemNotFoundError(f"Dish '{dish_name}' not found")

    inventory = load_inventory()
    ingredients = dishes[dish_name]

    result = []
    can_cook = True

    for item, qty in ingredients.items():
        required = qty * servings
        available = inventory.get(item, {}).get("quantity", 0)  # Safe: default 0
        enough = available >= required

        if not enough:
            can_cook = False

        result.append({
            "item": item,
            "required": required,
            "available": available,
            "enough": enough
        })

    return {
        "dish": dish_name,
        "servings": servings,
        "can_cook": can_cook,
        "ingredients": result
    }
