from kitchen.services.alert_system import check_alerts


def generate_shopping_list():
    alerts = check_alerts()

    if "error" in alerts:
        return alerts

    low_stock = alerts.get("low_stock", [])
    out_of_stock = alerts.get("out_of_stock", [])

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock
    }