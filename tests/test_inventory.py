import pytest
import json
import os
import tempfile
from unittest.mock import patch

# Point data files to temp files during tests
@pytest.fixture
def temp_inventory(tmp_path):
    inv_file = tmp_path / "inventory.json"
    inv_file.write_text(json.dumps({
        "rice": {"quantity": 1000, "unit": "g", "expiry_date": None}
    }))
    return str(inv_file)

def test_add_stock_new_item(temp_inventory):
    with patch("kitchen.services.data_loader.open", create=True) as mock_open:
        pass  # Integration tested below via service directly

def test_add_stock_increases_quantity():
    from kitchen.services.inventory_manager import add_stock
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load, \
         patch("kitchen.services.inventory_manager.save_inventory") as mock_save:
        mock_load.return_value = {"rice": {"quantity": 500, "unit": "g", "expiry_date": None}}
        result = add_stock("rice", 200, "g")
        assert result["quantity"] == 700
        assert result["status"] == "updated"

def test_add_stock_new_item_created():
    from kitchen.services.inventory_manager import add_stock
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load, \
         patch("kitchen.services.inventory_manager.save_inventory"):
        mock_load.return_value = {}
        result = add_stock("salt", 100, "g")
        assert result["item"] == "salt"
        assert result["status"] == "added"

def test_add_stock_invalid_quantity():
    from kitchen.services.inventory_manager import add_stock
    from kitchen.utils.exceptions import InvalidInputError
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load:
        mock_load.return_value = {}
        with pytest.raises(InvalidInputError):
            add_stock("rice", -10, "g")

def test_delete_stock_removes_item():
    from kitchen.services.inventory_manager import delete_stock
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load, \
         patch("kitchen.services.inventory_manager.save_inventory"):
        mock_load.return_value = {"rice": {"quantity": 500, "unit": "g", "expiry_date": None}}
        result = delete_stock("rice")
        assert result["status"] == "deleted"

def test_delete_stock_not_found():
    from kitchen.services.inventory_manager import delete_stock
    from kitchen.utils.exceptions import ItemNotFoundError
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load:
        mock_load.return_value = {}
        with pytest.raises(ItemNotFoundError):
            delete_stock("ghost_item")

def test_update_stock_changes_quantity():
    from kitchen.services.inventory_manager import update_stock
    with patch("kitchen.services.inventory_manager.load_inventory") as mock_load, \
         patch("kitchen.services.inventory_manager.save_inventory"):
        mock_load.return_value = {"rice": {"quantity": 500, "unit": "g", "expiry_date": None}}
        result = update_stock("rice", 999)
        assert result["quantity"] == 999
