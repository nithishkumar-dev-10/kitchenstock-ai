import json

# Load dishes
def load_dishes():
    with open("data/dishes.json") as f:
        return json.load(f)


# Load inventory
def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)


# Main function
def suggest_recipes(max_missing=2):
    dishes = load_dishes()
    inventory = load_inventory()

    available = []
    partial = []

    for dish_name, ingredients in dishes.items():
        missing_items = []

        for item in ingredients:
            available_qty = inventory.get(item, {}).get("quantity", 0)

            if available_qty <= 0:
                missing_items.append(item)

        # classify dishes
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