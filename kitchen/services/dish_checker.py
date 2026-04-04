import json

def check_ingredients(dish_name, servings):
    with open("data/dishes.json") as f:
        dishes = json.load(f)

    with open("data/inventory.json") as f:
        inventory = json.load(f)

    if dish_name not in dishes:
        return {
            "error": "Dish not found"
        }

    ingredients = dishes[dish_name]

    result = []
    can_cook = True

    for item, qty in ingredients.items():
        required = qty * servings
        available = inventory.get(item, {}).get("quantity", 0)

        item_status = {
            "item": item,
            "required": required,
            "available": available,
            "enough": available >= required
        }

        if available < required:
            can_cook = False

        result.append(item_status)

    return {
        "dish": dish_name,
        "servings": servings,
        "can_cook": can_cook,
        "ingredients": result
    }