import json
from kitchen.utils.exceptions import DataLoadError


def load_inventory() -> dict:
    try:
        with open("data/inventory.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataLoadError("Inventory data file not found")
    except json.JSONDecodeError:
        raise DataLoadError("Inventory data file is corrupted")


def load_dishes() -> dict:
    try:
        with open("data/dishes.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataLoadError("Dishes data file not found")
    except json.JSONDecodeError:
        raise DataLoadError("Dishes data file is corrupted")


def load_thresholds() -> dict:
    try:
        with open("data/thresholds.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise DataLoadError("Thresholds data file not found")
    except json.JSONDecodeError:
        raise DataLoadError("Thresholds data file is corrupted")


def save_inventory(inventory: dict) -> None:
    with open("data/inventory.json", "w") as f:
        json.dump(inventory, f, indent=4)
