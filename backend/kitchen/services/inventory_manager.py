from kitchen.services.data_loader import load_inventory, save_inventory, load_thresholds
from kitchen.utils.exceptions import ItemNotFoundError, InvalidInputError
from ml.ml_engine import predict_storage_type


def _predict_storage(item: str, quantity: float, thresholds: dict) -> str:
    threshold = float(thresholds.get(item, 100))
    ratio     = round(quantity / threshold, 3) if threshold > 0 else 1.0
    features  = {
        "used_g":                  0.0,
        "current_stock_g":         float(quantity),
        "threshold_g":             threshold,
        "avg_daily_usage_g":       10.0,
        "days_since_last_used":    1,
        "usage_last_7_days_g":     0.0,
        "stock_to_threshold_ratio": ratio,
        "is_weekend":              0,
    }
    return predict_storage_type(features)


def get_inventory() -> dict:
    return load_inventory()


def add_stock(item: str, quantity: float, unit: str, expiry_date: str = None) -> dict:
    if quantity <= 0:
        raise InvalidInputError("Quantity must be greater than 0")

    inventory  = load_inventory()
    thresholds = load_thresholds()

    if item in inventory:
        inventory[item]["quantity"] += quantity
        if expiry_date:
            inventory[item]["expiry_date"] = expiry_date
        status = "updated"
    else:
        storage_type = _predict_storage(item, quantity, thresholds)
        inventory[item] = {
            "quantity":    quantity,
            "unit":        unit,
            "expiry_date": expiry_date,
            "storage_type": storage_type
        }
        status = "added"

    save_inventory(inventory)

    return {
        "item":         item,
        "quantity":     inventory[item]["quantity"],
        "unit":         inventory[item]["unit"],
        "expiry_date":  inventory[item].get("expiry_date"),
        "storage_type": inventory[item].get("storage_type"),
        "status":       status
    }


def update_stock(item: str, quantity: float) -> dict:
    if quantity <= 0:
        raise InvalidInputError("Quantity must be greater than 0")

    inventory = load_inventory()

    if item not in inventory:
        raise ItemNotFoundError(f"Item '{item}' not found in inventory")

    inventory[item]["quantity"] = quantity
    save_inventory(inventory)

    return {
        "item":     item,
        "quantity": quantity,
        "unit":     inventory[item]["unit"],
        "status":   "updated"
    }


def delete_stock(item: str) -> dict:
    inventory = load_inventory()

    if item not in inventory:
        raise ItemNotFoundError(f"Item '{item}' not found in inventory")

    del inventory[item]
    save_inventory(inventory)

    return {"item": item, "status": "deleted"}