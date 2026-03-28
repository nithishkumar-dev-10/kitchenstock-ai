import json

# Load inventory
def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)


# Load thresholds
def load_thresholds():
    with open("data/thresholds.json") as f:
        return json.load(f)


#  Main function
def check_alerts():
    inventory = load_inventory()
    thresholds = load_thresholds()

    low_stock = []
    out_of_stock = []

    for item, data in inventory.items():
        quantity = data.get("quantity", 0)

        # get threshold (default = 1)
        threshold = thresholds.get(item, 1)

        if quantity == 0:
            out_of_stock.append(item)
        elif quantity < threshold:
            low_stock.append(item)

    # Print alerts
    print("\nInventory Alerts:\n")

    if out_of_stock:
        print("OUT OF STOCK:")
        for item in out_of_stock:
            print(f"- {item}")
        print()

    if low_stock:
        print("LOW STOCK:")
        for item in low_stock:
            print(f"- {item}")
        print()

    if not low_stock and not out_of_stock:
        print("All items are sufficiently stocked.\n")

    # Return structured data (IMPORTANT for next features)
    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock
    }