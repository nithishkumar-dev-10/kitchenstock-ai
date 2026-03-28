import json
from kitchen.services.dish_checker import check_ingredients


def cook_dish(dish_name, servings):
    if not check_ingredients(dish_name, servings):
        print(" Ingredients were insufficient earlier!")
        print(" Did you buy items? Consider updating inventory.")
    if not check_ingredients(dish_name, servings):
        print(" Cannot cook")
        return False

    with open("data/dishes.json") as f:
        dishes = json.load(f)

    with open("data/inventory.json") as f:
        inventory = json.load(f)

    # check dish exists
    if dish_name not in dishes:
        print("Dish not found")
        return

    ingredients = dishes[dish_name]

    for item, qty in ingredients.items():
        required = qty * servings

        if item in inventory:
            inventory[item]["quantity"] -= required

            # prevent negative values
            if inventory[item]["quantity"] < 0:
                inventory[item]["quantity"] = 0
        else:
            print(f" {item} not found in inventory")

    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

    print(" Cooking done & inventory updated")