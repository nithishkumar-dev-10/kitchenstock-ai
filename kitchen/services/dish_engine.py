import json
from kitchen.services.dish_checker import check_ingredients


def cook_dish(dish_name, servings):
    check_result = check_ingredients(dish_name, servings)

    # If dish not found or cannot cook
    if "error" in check_result:
        return check_result

    if not check_result["can_cook"]:
        return {
            "status": "failed",
            "message": "Insufficient ingredients",
            "details": check_result
        }

    with open("data/dishes.json") as f:
        dishes = json.load(f)

    with open("data/inventory.json") as f:
        inventory = json.load(f)

    ingredients = dishes[dish_name]

    updated_items = []

    for item, qty in ingredients.items():
        required = qty * servings

        if item in inventory:
            inventory[item]["quantity"] -= required

            # prevent negative
            if inventory[item]["quantity"] < 0:
                inventory[item]["quantity"] = 0

            updated_items.append({
                "item": item,
                "used": required,
                "remaining": inventory[item]["quantity"]
            })
        else:
            updated_items.append({
                "item": item,
                "error": "not found in inventory"
            })

    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

    return {
        "status": "success",
        "dish": dish_name,
        "servings": servings,
        "updated_inventory": updated_items
    }