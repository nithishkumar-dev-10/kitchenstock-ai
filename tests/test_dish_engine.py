import pytest
from unittest.mock import patch
from kitchen.utils.exceptions import InsufficientStockError, ItemNotFoundError


DISHES = {
    "poori": {"flour": 150, "oil": 50},
    "aloo_poori": {"flour": 150, "potato": 200, "oil": 50}
}

FULL_INVENTORY = {
    "flour": {"quantity": 1000, "unit": "g", "expiry_date": None},
    "oil":   {"quantity": 500,  "unit": "ml", "expiry_date": None},
    "potato":{"quantity": 1000, "unit": "g", "expiry_date": None},
}

def test_cook_dish_deducts_inventory():
    from kitchen.services.dish_engine import cook_dish
    inventory = {k: dict(v) for k, v in FULL_INVENTORY.items()}  # deep copy
    with patch("kitchen.services.dish_engine.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_engine.load_inventory", return_value=inventory), \
         patch("kitchen.services.dish_engine.save_inventory") as mock_save, \
         patch("kitchen.services.dish_checker.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_checker.load_inventory", return_value=inventory):
        result = cook_dish("poori", 2)
        assert result["dish_name"] == "poori"
        assert result["servings"] == 2
        saved = mock_save.call_args[0][0]
        assert saved["flour"]["quantity"] == 1000 - 150 * 2
        assert saved["oil"]["quantity"] == 500 - 50 * 2

def test_cook_dish_insufficient_stock():
    from kitchen.services.dish_engine import cook_dish
    low_inventory = {
        "flour": {"quantity": 10, "unit": "g", "expiry_date": None},
        "oil":   {"quantity": 500, "unit": "ml", "expiry_date": None},
    }
    with patch("kitchen.services.dish_checker.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_checker.load_inventory", return_value=low_inventory), \
         patch("kitchen.services.dish_engine.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_engine.load_inventory", return_value=low_inventory):
        with pytest.raises(InsufficientStockError):
            cook_dish("poori", 2)

def test_cook_dish_not_found():
    from kitchen.services.dish_engine import cook_dish
    with patch("kitchen.services.dish_checker.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_checker.load_inventory", return_value=FULL_INVENTORY):
        with pytest.raises(ItemNotFoundError):
            cook_dish("biryani", 1)

def test_cook_dish_clamps_to_zero():
    from kitchen.services.dish_engine import cook_dish
    tight_inventory = {
        "flour": {"quantity": 100, "unit": "g", "expiry_date": None},
        "oil":   {"quantity": 500, "unit": "ml", "expiry_date": None},
    }
    with patch("kitchen.services.dish_checker.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_checker.load_inventory", return_value=tight_inventory), \
         patch("kitchen.services.dish_engine.load_dishes", return_value=DISHES), \
         patch("kitchen.services.dish_engine.load_inventory", return_value={k: dict(v) for k, v in tight_inventory.items()}), \
         patch("kitchen.services.dish_engine.save_inventory") as mock_save:
        cook_dish("poori", 1)
        saved = mock_save.call_args[0][0]
        assert saved["flour"]["quantity"] >= 0
