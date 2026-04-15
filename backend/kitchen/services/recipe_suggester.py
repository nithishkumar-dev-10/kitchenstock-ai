
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
        total = len(ingredients)
        missing_items = []

        for item in ingredients:
            available_qty = inventory.get(item, {}).get("quantity", 0)
            if available_qty <= 0:
                missing_items.append(item)

        have = total - len(missing_items)
        coverage = round((have / total) * 100) if total > 0 else 0

        if len(missing_items) == 0:
            available.append({
                "dish": dish_name,
                "coverage_percent": 100,
                "total_ingredients": total
            })
        elif len(missing_items) <= max_missing:
            partial.append({
                "dish": dish_name,
                "coverage_percent": coverage,
                "missing_items": missing_items,
                "total_ingredients": total
            })

    # Sort by coverage descending
    available.sort(key=lambda x: x["coverage_percent"], reverse=True)
    partial.sort(key=lambda x: x["coverage_percent"], reverse=True)

    return {
        "available": available,
        "partial": partial
    }
