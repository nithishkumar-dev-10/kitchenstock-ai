import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle
from pathlib import Path

CSV_PATH   = Path(__file__).parent.parent / "data" / "training_data.csv"
MODEL_PATH = Path(__file__).parent / "model.pkl"

FEATURES = [
    "used_g",
    "current_stock_g",
    "threshold_g",
    "avg_daily_usage_g",
    "days_since_last_used",
    "usage_last_7_days_g",
    "stock_to_threshold_ratio",
    "is_weekend"
]
TARGET = "days_until_runout"


def train_model():
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=FEATURES + [TARGET])

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print(f"MAE: {mae:.2f} days | R²: {r2:.3f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved → {MODEL_PATH}")
    return model, mae, r2


def predict_days(ingredient_features: dict) -> float:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    row = pd.DataFrame([ingredient_features])[FEATURES]
    prediction = model.predict(row)[0]
    return round(float(prediction), 1)


if __name__ == "__main__":
    train_model()