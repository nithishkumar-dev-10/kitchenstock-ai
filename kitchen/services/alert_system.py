import json

# Load inventory
def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)


# Load thresholds
def load_thresholds():
    with open("data/thresholds.json") as f:
        return json.load(f)


# Main function
def check_alerts():
    inventory = load_inventory()
    thresholds = load_thresholds()

    low_stock = []
    out_of_stock = []

    for item, data in inventory.items():
        quantity = data.get("quantity", 0)

        # default threshold = 1
        threshold = thresholds.get(item, 1)

        if quantity == 0:
            out_of_stock.append(item)
        elif quantity < threshold:
            low_stock.append(item)

    return {
        "status": "ok",
        "alerts": {
            "low_stock": low_stock,
            "out_of_stock": out_of_stock
        }
    }