import json
from kitchen.services.dish_checker import check_ingredients


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


def save_inventory(inventory):
    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)


def cook_dish(dish_name, servings):
    check_result = check_ingredients(dish_name, servings)

    if "error" in check_result:
        return check_result

    if not check_result.get("can_cook"):
        return {"error": "Insufficient ingredients"}

    dishes = load_dishes()
    inventory = load_inventory()

    if dish_name not in dishes:
        return {"error": "Dish not found"}

    ingredients = dishes[dish_name]
    updated_items = []

    for item, qty in ingredients.items():
        required = qty * servings

        if item not in inventory:
            return {"error": f"{item} not found in inventory"}

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