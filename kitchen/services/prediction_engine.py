
from kitchen.services.data_loader import load_inventory, load_thresholds
from kitchen.services.consumption_analyzer import ConsumptionAnalyzer
from kitchen.utils.exceptions import NoDataAvailableError


def predict_runout() -> dict:
    inventory = load_inventory()

    if not inventory:
        raise NoDataAvailableError("Inventory is empty")

    thresholds = load_thresholds()
    analyzer = ConsumptionAnalyzer()
    daily_usage = analyzer.get_daily_usage()

    predictions = []

    for item, data in inventory.items():
        quantity = data.get("quantity", 0)
        usage_per_day = daily_usage.get(item, 0)
        threshold = thresholds.get(item, 0)

        if usage_per_day > 0:
            days_until_empty = round(quantity / usage_per_day, 1)
            days_until_low = round((quantity - threshold) / usage_per_day, 1) if threshold > 0 else None
        else:
            days_until_empty = None  # No usage data yet
            days_until_low = None

        # Assign urgency
        if days_until_empty is None:
            urgency = "UNKNOWN"
        elif days_until_empty <= 3:
            urgency = "HIGH"
        elif days_until_empty <= 7:
            urgency = "MEDIUM"
        else:
            urgency = "LOW"

        predictions.append({
            "item": item,
            "current_quantity": quantity,
            "unit": data.get("unit", ""),
            "daily_usage": usage_per_day,
            "days_until_empty": days_until_empty,
            "days_until_low_stock": days_until_low,
            "urgency": urgency
        })

    # Sort: HIGH first, then MEDIUM, then LOW, then UNKNOWN
    urgency_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "UNKNOWN": 3}
    predictions.sort(key=lambda x: urgency_order.get(x["urgency"], 3))

    return {"predictions": predictions}
