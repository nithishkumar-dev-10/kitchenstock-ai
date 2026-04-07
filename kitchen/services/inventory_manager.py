import json


def load_inventory():
    try:
        with open("data/inventory.json") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



def save_inventory(inventory):
    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)


def add_stock(item, quantity, unit):
    inventory = load_inventory()

  
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}

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



def get_inventory():
    return load_inventory()



def update_stock(item, quantity):
    inventory = load_inventory()


    if item not in inventory:
        return {"error": "Item not found"}

  
    if quantity <= 0:
        return {"error": "Quantity must be greater than 0"}

    inventory[item]["quantity"] = quantity
    save_inventory(inventory)

    return {
        "item": item,
        "quantity": quantity,
        "unit": inventory[item]["unit"],
        "status": "updated"
    }