import json


def load_inventory():
    try:
        with open("data/inventory.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def load_thresholds():
    try:
        with open("data/thresholds.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def check_alerts():
    inventory = load_inventory()
    thresholds = load_thresholds()

    if not inventory:
        return {"error": "Inventory is empty"}

    low_stock = []
    out_of_stock = []

    for item, data in inventory.items():
        quantity = data.get("quantity", 0)
        threshold = thresholds.get(item, 1)

        if quantity == 0:
            out_of_stock.append(item)
        elif quantity < threshold:
            low_stock.append(item)

    if not low_stock and not out_of_stock:
        message = "All items are in good condition"
    else:
        message = "Some items need attention: low stock or out of stock."

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "message": message
    }