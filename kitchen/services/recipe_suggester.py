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


def suggest_recipes(max_missing=2):
    dishes = load_dishes()
    inventory = load_inventory()

    if not dishes:
        return {"error": "No recipes available"}

    if max_missing < 0:
        return {"error": "max_missing must be >= 0"}

    available = []
    partial = []

    for dish_name, ingredients in dishes.items():
        missing_items = []

        for item in ingredients:
            available_qty = inventory.get(item, {}).get("quantity", 0)

            if available_qty <= 0:
                missing_items.append(item)

        if len(missing_items) == 0:
            available.append(dish_name)
        elif len(missing_items) <= max_missing:
            partial.append({
                "dish": dish_name,
                "missing_items": missing_items
            })

    return {
        "available": available,
        "partial": partial
    }