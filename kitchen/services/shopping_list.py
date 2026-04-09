from kitchen.services.alert_system import check_alerts
from kitchen.utils.exceptions import NoDataAvailableError


def generate_shopping_list() -> dict:
    # check_alerts() will raise DataLoadError or NoDataAvailableError
    alerts = check_alerts()

    low_stock = alerts.get("low_stock", [])
    out_of_stock = alerts.get("out_of_stock", [])

    if not low_stock and not out_of_stock:
        raise NoDataAvailableError("Everything is well stocked — no shopping needed")

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock
    
    }
