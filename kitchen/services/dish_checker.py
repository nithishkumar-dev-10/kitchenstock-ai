import json

def check_ingredients(dish_name, servings):
    with open("data/dishes.json") as f:
        dishes = json.load(f)

    with open("data/inventory.json") as f:
        inventory = json.load(f)

    
    if dish_name not in dishes:
        print("Dish not found")
        return False

    ingredients = dishes[dish_name]

    print(f"\nChecking ingredients for {dish_name} ({servings} servings):\n")

    can_cook = True

    for item, qty in ingredients.items():
        required = qty * servings
        available = inventory.get(item, {}).get("quantity", 0)

        if available >= required:
            print(f"✅ {item}: need {required}, have {available}")
        else:
            print(f"❌ {item}: need {required}, have {available}")
            can_cook = False

    return can_cook