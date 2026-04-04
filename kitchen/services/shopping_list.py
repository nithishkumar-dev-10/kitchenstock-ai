from kitchen.services.alert_system import check_alerts


def generate_shopping_list():
    alerts = check_alerts()

    
    low_stock = alerts["alerts"]["low_stock"]
    out_of_stock = alerts["alerts"]["out_of_stock"]

    return {
        "status": "ok",
        "shopping_list": {
            "low_stock": low_stock,
            "out_of_stock": out_of_stock
        }
    }