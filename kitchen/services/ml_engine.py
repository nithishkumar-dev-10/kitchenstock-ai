import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from ml.ml_engine import predict_days
from kitchen.services.consumption_analyzer import ConsumptionAnalyzer
from kitchen.services.data_loader import load_inventory, load_thresholds
from pathlib import Path
import pickle

MODEL_PATH = Path(__file__).resolve().parent.parent.parent / "ml" / "model.pkl"


def is_model_trained() -> bool:
    return MODEL_PATH.exists()


def predict_with_model() -> dict:
    if not is_model_trained():
        return {"error": "Model not trained yet. Run: python ml/ml_engine.py"}

    inventory  = load_inventory()
    thresholds = load_thresholds()
    analyzer   = ConsumptionAnalyzer()
    daily_usage = analyzer.get_daily_usage()

    predictions = []

    for ingredient, data in inventory.items():
        stock     = data.get("quantity", 0)
        threshold = thresholds.get(ingredient, 0)
        avg_daily = daily_usage.get(ingredient, 0)
        usage_7d  = avg_daily * 7
        ratio     = round(stock / threshold, 3) if threshold > 0 else 1.0

        features = {
            "used_g":                   avg_daily,
            "current_stock_g":          stock,
            "threshold_g":              threshold,
            "avg_daily_usage_g":        avg_daily,
            "days_since_last_used":     1,
            "usage_last_7_days_g":      usage_7d,
            "stock_to_threshold_ratio": ratio,
            "is_weekend":               0
        }

        try:
            days = predict_days(features)
        except Exception:
            days = None

        predictions.append({
            "item":              ingredient,
            "current_quantity":  stock,
            "unit":              data.get("unit", ""),
            "ml_days_until_runout": days,
            "status": (
                "critical" if days is not None and days <= 3
                else "warning"  if days is not None and days <= 7
                else "safe"
            )
        })

    predictions.sort(key=lambda x: (x["ml_days_until_runout"] or 999))
    return {"predictions": predictions}