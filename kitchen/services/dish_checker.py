import json
from kitchen.utils.exceptions import ItemNotFoundError, InvalidInputError, DataLoadError


def load_dishes() -> dict:
    try:
        with open("data/dishes.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataLoadError("Dishes data file not found")
    except json.JSONDecodeError:
        raise DataLoadError("Dishes data file is corrupted")


def load_inventory() -> dict:
    try:
        with open("data/inventory.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataLoadError("Inventory data file not found")
    except json.JSONDecodeError:
        raise DataLoadError("Inventory data file is corrupted")


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
        available = inventory.get(item, {}).get("quantity", 0)
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