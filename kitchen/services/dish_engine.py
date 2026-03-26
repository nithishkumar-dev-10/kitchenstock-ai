import json

def cook_dish(dish_name, servings):
    with open("data/dishes.json") as f:
        dishes = json.load(f)

    with open("data/inventory.json") as f:
        inventory = json.load(f)

    ingredients = dishes[dish_name]

    for item, qty in ingredients.items():
        inventory[item] -= qty * servings

    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)

    print("Done")