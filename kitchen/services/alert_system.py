from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.utils.exceptions import NoDataAvailableError


def check_alerts() -> dict:
    inventory = load_inventory()

    if not inventory:
        raise NoDataAvailableError("Inventory is empty — nothing to check")

    thresholds = load_thresholds()

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
        message = "Some items need attention: low stock or out of stock"

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "message": message
    }
