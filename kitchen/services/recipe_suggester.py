from kitchen.services.data_loader import load_dishes, load_inventory
from kitchen.utils.exceptions import InvalidInputError, NoDataAvailableError


def suggest_recipes(max_missing: int = 2) -> dict:
    if max_missing < 0:
        raise InvalidInputError("max_missing must be 0 or greater")

    dishes = load_dishes()

    if not dishes:
        raise NoDataAvailableError("No recipes available in the system")

    inventory = load_inventory()

    available = []
    partial = []

    for dish_name, ingredients in dishes.items():
        missing_items = []

        for item in ingredients:
            available_qty = inventory.get(item, {}).get("quantity", 0)  # Safe default

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
