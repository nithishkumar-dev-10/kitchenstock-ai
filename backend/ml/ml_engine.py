import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, classification_report, accuracy_score
import pickle
from pathlib import Path

CSV_PATH        = Path(__file__).parent.parent / "data" / "training_data.csv"
MODEL_PATH      = Path(__file__).parent / "model.pkl"
CLASSIFIER_PATH = Path(__file__).parent / "classifier_model.pkl"
ENCODER_PATH    = Path(__file__).parent / "label_encoder.pkl"

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

REGRESSOR_TARGET  = "days_until_runout"
CLASSIFIER_TARGET = "storage_type"


# ── REGRESSOR (existing, unchanged) ──────────────────────────
def train_model():
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=FEATURES + [REGRESSOR_TARGET])

    X = df[FEATURES]
    y = df[REGRESSOR_TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2  = r2_score(y_test, y_pred)

    print(f"Regressor → MAE: {mae:.2f} days | R²: {r2:.3f}")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    print(f"Regressor saved → {MODEL_PATH}")
    return model, mae, r2


def predict_days(ingredient_features: dict) -> float:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    row = pd.DataFrame([ingredient_features])[FEATURES]
    prediction = model.predict(row)[0]
    return round(float(prediction), 1)


# ── CLASSIFIER (new) ─────────────────────────────────────────
def train_classifier():
    df = pd.read_csv(CSV_PATH)
    df = df.dropna(subset=FEATURES + [CLASSIFIER_TARGET])
    df = df[df[CLASSIFIER_TARGET].isin(["fridge", "freezer", "room_temp"])]

    X = df[FEATURES]
    y = df[CLASSIFIER_TARGET]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"Classifier → Accuracy: {acc:.3f}")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    with open(CLASSIFIER_PATH, "wb") as f:
        pickle.dump(clf, f)

    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(le, f)

    print(f"Classifier saved → {CLASSIFIER_PATH}")
    print(f"Encoder saved    → {ENCODER_PATH}")
    return clf, le, acc


def predict_storage_type(ingredient_features: dict) -> str:
    with open(CLASSIFIER_PATH, "rb") as f:
        clf = pickle.load(f)

    with open(ENCODER_PATH, "rb") as f:
        le = pickle.load(f)

    row = pd.DataFrame([ingredient_features])[FEATURES]
    prediction_encoded = clf.predict(row)[0]
    label = le.inverse_transform([prediction_encoded])[0]
    return label


# ── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Training Regressor ===")
    train_model()
    print("\n=== Training Classifier ===")
    train_classifier()