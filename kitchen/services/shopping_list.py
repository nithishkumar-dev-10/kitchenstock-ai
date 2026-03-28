from kitchen.services.alert_system import check_alerts


def generate_shopping_list():
    alerts = check_alerts()

    low_stock = alerts["low_stock"]
    out_of_stock = alerts["out_of_stock"]

    print("\nSHOPPING LIST:\n")

    if out_of_stock:
        print("OUT OF STOCK:")
        for item in out_of_stock:
            print(f"- {item}")
        print()

    if low_stock:
        print("LOW STOCK:")
        for item in low_stock:
            print(f"- {item}")
        print()

    if not low_stock and not out_of_stock:
        print("No items in inventory is low stock.\n")

    return {
        "low_stock": low_stock,
        "out_of_stock": out_of_stock
    }