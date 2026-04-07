import json


def load_dishes():
    try:
        with open("data/dishes.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_inventory():
    try:
        with open("data/inventory.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def check_ingredients(dish_name, servings):
    dishes = load_dishes()
    inventory = load_inventory()

    if dish_name not in dishes:
        return {"error": "Dish not found"}

    if servings <= 0:
        return {"error": "Servings must be greater than 0"}

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