import json


# Load inventory
def load_inventory():
    with open("data/inventory.json") as f:
        return json.load(f)


# Save inventory
def save_inventory(inventory):
    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)


# Add or update stock
def add_stock(item, quantity, unit):
    inventory = load_inventory()

    if item in inventory:
        inventory[item]["quantity"] += quantity
        print(f"Updated {item}: +{quantity} {unit}")
    else:
        inventory[item] = {
            "quantity": quantity,
            "unit": unit
        }
        print(f"Added new item: {item} ({quantity} {unit})")

    save_inventory(inventory)


# Get full inventory
def get_inventory():
    return load_inventory()


# Print inventory (for debugging)
def print_inventory():
    inventory = load_inventory()

    print("\nCurrent Inventory:\n")

    for item, data in inventory.items():
        print(f"{item}: {data['quantity']} {data['unit']}")

    print()


# Update specific item quantity
def update_stock(item, quantity):
    inventory = load_inventory()

    if item in inventory:
        inventory[item]["quantity"] = quantity
        print(f"Updated {item} to {quantity}")
    else:
        print(f"{item} not found")

    save_inventory(inventory)