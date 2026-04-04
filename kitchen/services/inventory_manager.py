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
        status = "updated"
    else:
        inventory[item] = {
            "quantity": quantity,
            "unit": unit
        }
        status = "added"

    save_inventory(inventory)

    return {
        "item": item,
        "quantity": inventory[item]["quantity"],
        "unit": inventory[item]["unit"],
        "status": status
    }


# Get full inventory
def get_inventory():
    return load_inventory()


# Update specific item quantity
def update_stock(item, quantity):
    inventory = load_inventory()

    if item in inventory:
        inventory[item]["quantity"] = quantity
        save_inventory(inventory)

        return {
            "item": item,
            "quantity": quantity,
            "status": "updated"
        }
    else:
        return {
            "error": f"{item} not found"
        }