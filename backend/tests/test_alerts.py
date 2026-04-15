import pytest
from unittest.mock import patch
from kitchen.utils.exceptions import NoDataAvailableError


def test_no_alerts_when_all_good():
    from kitchen.services.alert_system import check_alerts
    with patch("kitchen.services.alert_system.load_inventory") as mock_inv, \
         patch("kitchen.services.alert_system.load_thresholds") as mock_thr:
        mock_inv.return_value = {
            "rice": {"quantity": 5000, "unit": "g", "expiry_date": None}
        }
        mock_thr.return_value = {"rice": 1000}
        result = check_alerts()
        assert result["low_stock"] == []
        assert result["out_of_stock"] == []

def test_low_stock_detected():
    from kitchen.services.alert_system import check_alerts
    with patch("kitchen.services.alert_system.load_inventory") as mock_inv, \
         patch("kitchen.services.alert_system.load_thresholds") as mock_thr:
        mock_inv.return_value = {
            "rice": {"quantity": 500, "unit": "g", "expiry_date": None}
        }
        mock_thr.return_value = {"rice": 1000}
        result = check_alerts()
        assert "rice" in result["low_stock"]

def test_out_of_stock_detected():
    from kitchen.services.alert_system import check_alerts
    with patch("kitchen.services.alert_system.load_inventory") as mock_inv, \
         patch("kitchen.services.alert_system.load_thresholds") as mock_thr:
        mock_inv.return_value = {
            "salt": {"quantity": 0, "unit": "g", "expiry_date": None}
        }
        mock_thr.return_value = {"salt": 100}
        result = check_alerts()
        assert "salt" in result["out_of_stock"]

def test_expiry_alert_fires():
    from kitchen.services.alert_system import check_alerts
    from datetime import date, timedelta
    expiry = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    with patch("kitchen.services.alert_system.load_inventory") as mock_inv, \
         patch("kitchen.services.alert_system.load_thresholds") as mock_thr:
        mock_inv.return_value = {
            "chicken": {"quantity": 500, "unit": "g", "expiry_date": expiry}
        }
        mock_thr.return_value = {}
        result = check_alerts()
        assert len(result["expiring_soon"]) == 1
        assert result["expiring_soon"][0]["item"] == "chicken"

def test_empty_inventory_raises():
    from kitchen.services.alert_system import check_alerts
    with patch("kitchen.services.alert_system.load_inventory") as mock_inv:
        mock_inv.return_value = {}
        with pytest.raises(NoDataAvailableError):
            check_alerts()
