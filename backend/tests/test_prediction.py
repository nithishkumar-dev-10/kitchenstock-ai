
import pytest
from unittest.mock import patch, MagicMock


INVENTORY = {
    "rice": {"quantity": 1400, "unit": "g", "expiry_date": None},
    "oil":  {"quantity": 200,  "unit": "ml", "expiry_date": None},
}

THRESHOLDS = {
    "rice": 500,
    "oil": 100
}


def test_predict_returns_all_items():
    from kitchen.services.prediction_engine import predict_runout
    with patch("kitchen.services.prediction_engine.load_inventory", return_value=INVENTORY), \
         patch("kitchen.services.prediction_engine.load_thresholds", return_value=THRESHOLDS), \
         patch("kitchen.services.prediction_engine.ConsumptionAnalyzer") as MockCA:
        MockCA.return_value.get_daily_usage.return_value = {"rice": 200, "oil": 50}
        result = predict_runout()
        items = [p["item"] for p in result["predictions"]]
        assert "rice" in items
        assert "oil" in items


def test_predict_days_calculation():
    from kitchen.services.prediction_engine import predict_runout
    with patch("kitchen.services.prediction_engine.load_inventory", return_value=INVENTORY), \
         patch("kitchen.services.prediction_engine.load_thresholds", return_value=THRESHOLDS), \
         patch("kitchen.services.prediction_engine.ConsumptionAnalyzer") as MockCA:
        MockCA.return_value.get_daily_usage.return_value = {"rice": 200, "oil": 50}
        result = predict_runout()
        rice = next(p for p in result["predictions"] if p["item"] == "rice")
        assert rice["days_until_empty"] == 7.0


def test_predict_urgency_high():
    from kitchen.services.prediction_engine import predict_runout
    low_inv = {"rice": {"quantity": 300, "unit": "g", "expiry_date": None}}
    with patch("kitchen.services.prediction_engine.load_inventory", return_value=low_inv), \
         patch("kitchen.services.prediction_engine.load_thresholds", return_value={}), \
         patch("kitchen.services.prediction_engine.ConsumptionAnalyzer") as MockCA:
        MockCA.return_value.get_daily_usage.return_value = {"rice": 200}
        result = predict_runout()
        rice = next(p for p in result["predictions"] if p["item"] == "rice")
        assert rice["urgency"] == "HIGH"


def test_predict_unknown_when_no_usage():
    from kitchen.services.prediction_engine import predict_runout
    with patch("kitchen.services.prediction_engine.load_inventory", return_value=INVENTORY), \
         patch("kitchen.services.prediction_engine.load_thresholds", return_value=THRESHOLDS), \
         patch("kitchen.services.prediction_engine.ConsumptionAnalyzer") as MockCA:
        MockCA.return_value.get_daily_usage.return_value = {}  # no logs yet
        result = predict_runout()
        for p in result["predictions"]:
            assert p["urgency"] == "UNKNOWN"
            assert p["days_until_empty"] is None


def test_predict_sorted_by_urgency():
    from kitchen.services.prediction_engine import predict_runout
    inv = {
        "rice": {"quantity": 100, "unit": "g", "expiry_date": None},
        "oil":  {"quantity": 5000, "unit": "ml", "expiry_date": None},
    }
    with patch("kitchen.services.prediction_engine.load_inventory", return_value=inv), \
         patch("kitchen.services.prediction_engine.load_thresholds", return_value={}), \
         patch("kitchen.services.prediction_engine.ConsumptionAnalyzer") as MockCA:
        MockCA.return_value.get_daily_usage.return_value = {"rice": 200, "oil": 50}
        result = predict_runout()
        urgencies = [p["urgency"] for p in result["predictions"]]
        order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "UNKNOWN": 3}
        assert urgencies == sorted(urgencies, key=lambda u: order.get(u, 3))
