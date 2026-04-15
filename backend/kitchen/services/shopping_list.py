
from kitchen.services.alert_system import check_alerts
from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.utils.exceptions import NoDataAvailableError


def generate_shopping_list() -> dict:
    alerts = check_alerts()

    low_stock = alerts.get("low_stock", [])
    out_of_stock = alerts.get("out_of_stock", [])

    if not low_stock and not out_of_stock:
        raise NoDataAvailableError("Everything is well stocked — no shopping needed")

    inventory = load_inventory()
    thresholds = load_thresholds()

    def build_item(name, status):
        current = inventory.get(name, {}).get("quantity", 0)
        unit = inventory.get(name, {}).get("unit", "")
        threshold = thresholds.get(name, 0)
        # Suggest buying enough to reach 2x the threshold
        suggested_buy = max(0, round((threshold * 2) - current))
        return {
            "item": name,
            "current_quantity": current,
            "unit": unit,
            "suggested_buy": suggested_buy,
            "status": status
        }

    return {
        "out_of_stock": [build_item(i, "out_of_stock") for i in out_of_stock],
        "low_stock": [build_item(i, "low_stock") for i in low_stock]
    }
