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

        # --- Calculation ---
        if usage_per_day > 0:
            days_until_empty = round(quantity / usage_per_day, 1)
            days_until_low = (
                round((quantity - threshold) / usage_per_day, 1)
                if threshold > 0 else None
            )
            days_left = int(days_until_empty)
        else:
            days_until_empty = None
            days_until_low = None
            days_left = None

        # --- Urgency ---
        if days_until_empty is None:
            urgency = "UNKNOWN"
        elif days_until_empty <= 3:
            urgency = "HIGH"
        elif days_until_empty <= 7:
            urgency = "MEDIUM"
        else:
            urgency = "LOW"

        # --- Action ---
        if urgency == "HIGH":
            action = "Buy immediately"
        elif urgency == "MEDIUM":
            action = "Buy within a few days"
        elif urgency == "LOW":
            action = "Stock is sufficient"
        else:
            action = "Not enough data"

        # --- Status (for UI) ---
        status = (
            "critical" if urgency == "HIGH"
            else "warning" if urgency == "MEDIUM"
            else "safe" if urgency == "LOW"
            else "unknown"
        )

        predictions.append({
            "item": item,
            "current_quantity": quantity,
            "unit": data.get("unit", ""),
            "daily_usage": usage_per_day,
            "days_left": days_left,
            "days_until_empty": days_until_empty,
            "days_until_low_stock": days_until_low,
            "urgency": urgency,
            "action": action,
            "status": status
        })

    # --- Sorting ---
    urgency_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "UNKNOWN": 3}
    predictions.sort(key=lambda x: urgency_order.get(x["urgency"], 3))

    return {"predictions": predictions}