from ml.ml_engine import predict_storage_type
from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.utils.exceptions import ItemNotFoundError


STORAGE_MESSAGES = {
    "fridge":    "Store in the refrigerator (0–5°C).",
    "freezer":   "Store in the freezer (below -18°C).",
    "room_temp": "Store at room temperature in a cool, dry place.",
}

# ── HARDCODED OVERRIDES ───────────────────────────────────────────────────────
# For items where storage is a biological/physical fact — not something to predict.
# The ML model will never be reliable for these without massive domain-specific data.
# Add any new item here if you know its storage type for certain.
STORAGE_OVERRIDES = {
    # Freezer items
    "ice_cream":     "freezer",
    "frozen_peas":   "freezer",
    "frozen_corn":   "freezer",
    "chicken":       "freezer",
    "mutton":        "freezer",
    "fish":          "freezer",
    "prawns":        "freezer",

    # Fridge items
    "milk":          "fridge",
    "curd":          "fridge",
    "butter":        "fridge",
    "cheese":        "fridge",
    "paneer":        "fridge",
    "egg":           "fridge",
    "coconut_milk":  "fridge",
    "curry_leaves":  "fridge",
    "cucumber":      "fridge",
    "lettuce":       "fridge",
    "carrot":        "fridge",
    "capsicum":      "fridge",
    "tomato":        "fridge",
    "lemon":         "fridge",
    "apple":         "fridge",
    "banana":        "fridge",
    "mango":         "fridge",
    "orange":        "fridge",
    "coconut":       "fridge",
    "peas":          "fridge",
    "beans":         "fridge",

    # Room temp items
    "chocolate":     "room_temp",
    "rice":          "room_temp",
    "idli_rice":     "room_temp",
    "basmati_rice":  "room_temp",
    "toor_dal":      "room_temp",
    "urad_dal":      "room_temp",
    "moong_dal":     "room_temp",
    "flour":         "room_temp",
    "sugar":         "room_temp",
    "salt":          "room_temp",
    "oil":           "room_temp",
    "ghee":          "room_temp",
    "onion":         "room_temp",
    "potato":        "room_temp",
    "garlic":        "room_temp",
    "garam_masala":  "room_temp",
    "cumin":         "room_temp",
    "black_pepper":  "room_temp",
    "tamarind":      "room_temp",
    "urad_dal":      "room_temp",
    "semolina":      "room_temp",
    "noodles":       "room_temp",
    "pasta":         "room_temp",
    "bread":         "room_temp",
    "jam":           "room_temp",
    "soy_sauce":     "room_temp",
    "hing":          "room_temp",
}
# ─────────────────────────────────────────────────────────────────────────────


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


def _resolve_storage_type(item_name: str, features: dict) -> str:
    """
    Priority:
    1. Hardcoded override (always correct for known items)
    2. ML model prediction (fallback for unknown items)
    """
    if item_name in STORAGE_OVERRIDES:
        return STORAGE_OVERRIDES[item_name]

    return predict_storage_type(features)


def get_storage_advice(item_name: str) -> dict:
    inventory  = load_inventory()
    thresholds = load_thresholds()

    if item_name not in inventory:
        raise ItemNotFoundError(f"Item '{item_name}' not found in inventory")

    features     = _build_features(item_name, inventory, thresholds)
    storage_type = _resolve_storage_type(item_name, features)

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
            storage_type = _resolve_storage_type(item_name, features)
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
