from datetime import datetime
from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.utils.exceptions import NoDataAvailableError


def check_alerts() -> dict:
    inventory = load_inventory()

    if not inventory:
        raise NoDataAvailableError("Inventory is empty — nothing to check")

    thresholds = load_thresholds()

    low_stock = []
    out_of_stock = []
    expiring_soon = []

    today = datetime.today().date()
    alert_days = 3

    for item, data in inventory.items():
        quantity = data.get("quantity", 0)
        threshold = thresholds.get(item, 1)
        expiry_date = data.get("expiry_date")

        if quantity == 0:
            out_of_stock.append(item)
        elif quantity < threshold:
            low_stock.append(item)

        if expiry_date:
            try:
                expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                days_left = (expiry - today).days
                if days_left <= alert_days:
                    expiring_soon.append({
                        "item": item,
                        "expiry_date": expiry_date,
                        "days_left": days_left
                    })
            except ValueError:
                pass

    if not low_stock and not out_of_stock and not expiring_soon:
        message = "All items are in good condition"
    else:
        message = "Some items need attention"

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "expiring_soon": expiring_soon,
        "message": message
    }