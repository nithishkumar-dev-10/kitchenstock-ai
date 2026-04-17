from ml.ml_engine import predict_storage_type
from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.utils.exceptions import ItemNotFoundError


STORAGE_MESSAGES = {
    "fridge":    "Store in the refrigerator (0–5°C).",
    "freezer":   "Store in the freezer (below -18°C).",
    "room_temp": "Store at room temperature in a cool, dry place.",
}


def _build_features(item_name: str, inventory: dict, thresholds: dict) -> dict:
    quantity  = float(inventory.get(item_name, {}).get("quantity", 0))
    threshold = float(thresholds.get(item_name, 100))
    ratio     = round(quantity / threshold, 3) if threshold > 0 else 1.0

    return {
        "used_g":                  0.0,
        "current_stock_g":         quantity,
        "threshold_g":             threshold,
        "avg_daily_usage_g":       10.0,
        "days_since_last_used":    1,
        "usage_last_7_days_g":     0.0,
        "stock_to_threshold_ratio": ratio,
        "is_weekend":              0,
    }


def get_storage_advice(item_name: str) -> dict:
    inventory  = load_inventory()
    thresholds = load_thresholds()

    if item_name not in inventory:
        raise ItemNotFoundError(f"Item '{item_name}' not found in inventory")

    features     = _build_features(item_name, inventory, thresholds)
    storage_type = predict_storage_type(features)

    return {
        "item":         item_name,
        "storage_type": storage_type,
        "advice":       STORAGE_MESSAGES.get(storage_type, "Store safely.")
    }


def get_all_storage_advice(inventory: dict) -> dict:
    thresholds = load_thresholds()
    result     = {}

    for item_name in inventory:
        try:
            features     = _build_features(item_name, inventory, thresholds)
            storage_type = predict_storage_type(features)
            result[item_name] = {
                "storage_type": storage_type,
                "advice":       STORAGE_MESSAGES.get(storage_type, "Store safely.")
            }
        except Exception:
            result[item_name] = {
                "storage_type": "room_temp",
                "advice":       "Store at room temperature in a cool, dry place."
            }

    return result