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

    best_matches = []
    partial_matches = []

    for dish_name, ingredients in dishes.items():
        missing_items = []

        for item in ingredients:
            available = inventory.get(item, {}).get("quantity", 0)

            if available <= 0:
                missing_items.append(item)

        # classify dishes
        if len(missing_items) == 0:
            best_matches.append(dish_name)
        elif len(missing_items) <= max_missing:
            partial_matches.append((dish_name, missing_items))

    # Print suggestions
    print("\nRECIPE SUGGESTIONS:\n")

    if best_matches:
        print("AVAILABLE TO COOK:")
        for dish in best_matches:
            print(f"- {dish}")
        print()

    if partial_matches:
        print("CAN COOK WITH FEW MISSING ITEMS:")
        for dish, missing in partial_matches:
            print(f"- {dish} (missing: {', '.join(missing)})")
        print()

    if not best_matches and not partial_matches:
        print("No suitable recipes found with the current inventory .\n")

    # Return structured data
    return {
        "available": best_matches,
        "partial": partial_matches
    }