"""
ml/data_builder.py
------------------
Reads your 4 JSON files and produces data/training_data.csv
Run from project root: python ml/data_builder.py
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

# ── File paths ────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent
LOG_FILE      = ROOT / "data" / "consumption_log.json"
DISHES_FILE   = ROOT / "data" / "dishes.json"
INVENTORY_FILE= ROOT / "data" / "inventory.json"
THRESHOLD_FILE= ROOT / "data" / "thresholds.json"
OUTPUT_CSV    = ROOT / "data" / "training_data.csv"

# ── Step A: Unit conversion table (count → grams) ─────────
COUNT_TO_GRAMS = {
    "egg":    60,
    "bread":  30,
    "banana": 120,
    "apple":  180,
    "orange": 150,
    "mango":  200,
    "lemon":  60,
}

STORAGE_LABELS = {
    # ── Freezer ──────────────────────────────
    "chicken":           "freezer",
    "fish":              "freezer",
    "mutton":            "freezer",
    "ice_cream":         "freezer",

    # ── Fridge ───────────────────────────────
    "egg":               "fridge",
    "milk":              "fridge",
    "curd":              "fridge",
    "butter":            "fridge",
    "cheese":            "fridge",
    "paneer":            "fridge",
    "mayonnaise":        "fridge",
    "coconut_milk":      "fridge",
    "carrot":            "fridge",
    "beans":             "fridge",
    "tomato":            "fridge",
    "capsicum":          "fridge",
    "cabbage":           "fridge",
    "cauliflower":       "fridge",
    "spinach":           "fridge",
    "brinjal":           "fridge",
    "cucumber":          "fridge",
    "lettuce":           "fridge",
    "mushroom":          "fridge",
    "green_chili":       "fridge",
    "corn":              "fridge",
    "peas":              "fridge",
    "ginger":            "fridge",
    "garlic":            "fridge",
    "curry_leaves":      "fridge",
    "coconut":           "fridge",
    "lemon":             "fridge",
    "apple":             "fridge",
    "orange":            "fridge",
    "mango":             "fridge",
    "banana":            "fridge",
    "bread":             "fridge",

    # ── Room Temp ─────────────────────────────
    "rice":              "room_temp",
    "basmati_rice":      "room_temp",
    "brown_rice":        "room_temp",
    "idli_rice":         "room_temp",
    "wheat":             "room_temp",
    "flour":             "room_temp",
    "maida":             "room_temp",
    "rava":              "room_temp",
    "semolina":          "room_temp",
    "oats":              "room_temp",
    "noodles":           "room_temp",
    "pasta":             "room_temp",
    "toor_dal":          "room_temp",
    "moong_dal":         "room_temp",
    "chana_dal":         "room_temp",
    "urad_dal":          "room_temp",
    "rajma":             "room_temp",
    "chickpeas":         "room_temp",
    "onion":             "room_temp",
    "potato":            "room_temp",
    "oil":               "room_temp",
    "ghee":              "room_temp",
    "salt":              "room_temp",
    "sugar":             "room_temp",
    "jaggery":           "room_temp",
    "honey":             "room_temp",
    "turmeric":          "room_temp",
    "chili_powder":      "room_temp",
    "garam_masala":      "room_temp",
    "coriander_powder":  "room_temp",
    "cumin":             "room_temp",
    "mustard_seeds":     "room_temp",
    "black_pepper":      "room_temp",
    "cardamom":          "room_temp",
    "cloves":            "room_temp",
    "tamarind":          "room_temp",
    "hing":              "room_temp",
    "peanut":            "room_temp",
    "cashew":            "room_temp",
    "almond":            "room_temp",
    "chocolate":         "room_temp",
    "jam":               "room_temp",
    "soy_sauce":         "room_temp",
    "vinegar":           "room_temp",
    "tomato_ketchup":    "room_temp",
    "chili_sauce":       "room_temp",
    "mustard_sauce":     "room_temp",
}


def load_files():
    logs      = json.loads(LOG_FILE.read_text())
    dishes    = json.loads(DISHES_FILE.read_text())
    inventory = json.loads(INVENTORY_FILE.read_text())
    thresholds= json.loads(THRESHOLD_FILE.read_text())
    return logs, dishes, inventory, thresholds


def convert_to_grams(ingredient, quantity):
    if ingredient in COUNT_TO_GRAMS:
        return quantity * COUNT_TO_GRAMS[ingredient]
    return quantity


def remove_duplicate_logs(logs):
    seen = set()
    clean_logs = []
    for entry in logs:
        key = (entry["dish"], entry["date"])
        if key not in seen:
            seen.add(key)
            clean_logs.append(entry)
    return clean_logs


def flatten_logs(logs, dishes):
    flat = []

    for entry in logs:
        dish_name = entry["dish"]
        servings  = entry["servings"]
        date      = entry["date"]

        if dish_name not in dishes:
            continue

        for ingredient, qty_per_serving in dishes[dish_name].items():
            if ingredient == "steps":
                continue

            total_used = qty_per_serving * servings
            total_used_g = convert_to_grams(ingredient, total_used)

            flat.append({
                "date": date,
                "ingredient": ingredient,
                "used_g": round(total_used_g, 2)
            })

    return flat


def build_daily_usage(flat_logs):
    usage = defaultdict(lambda: defaultdict(float))

    for entry in flat_logs:
        usage[entry["ingredient"]][entry["date"]] += entry["used_g"]

    return usage


def build_training_csv(usage, inventory, thresholds):
    rows = []

    all_dates = sorted({
        d for m in usage.values() for d in m
    })

    for ingredient, date_map in usage.items():

        raw_stock = inventory.get(ingredient, {}).get("quantity", 0)
        stock_g = convert_to_grams(ingredient, raw_stock)

        raw_threshold = thresholds.get(ingredient, 0)
        threshold_g = convert_to_grams(ingredient, raw_threshold)

        total_used = sum(date_map.values())
        num_days = len(all_dates)
        avg_daily_g = round(total_used / num_days, 2)

        if avg_daily_g > 0:
            days_until_runout = min(round(stock_g / avg_daily_g, 1), 90)
        else:
            days_until_runout = 90

        for date in all_dates:
            rows.append({
                "date": date,
                "ingredient": ingredient,
                "used_g": round(date_map.get(date, 0), 2),
                "current_stock_g": round(stock_g, 2),
                "threshold_g": round(threshold_g, 2),
                "avg_daily_usage_g": avg_daily_g,
                "days_until_runout": days_until_runout,
                "storage_type": STORAGE_LABELS.get(ingredient, "room_temp"),
        })

    return rows


#  NEW FEATURE ENGINEERING FUNCTION
def add_features(rows, usage):

    # Precompute usage dates
    usage_dates = {}
    for ingredient, date_map in usage.items():
        usage_dates[ingredient] = sorted([d for d, g in date_map.items() if g > 0])

    enriched = []

    for row in rows:
        ingredient = row["ingredient"]
        date_str = row["date"]
        current_date = datetime.strptime(date_str, "%Y-%m-%d")

        # Feature 1: days_since_last_used
        active_dates = usage_dates.get(ingredient, [])
        past_dates = [d for d in active_dates if d < date_str]

        if past_dates:
            last_used = datetime.strptime(past_dates[-1], "%Y-%m-%d")
            days_since = (current_date - last_used).days
        else:
            days_since = 99

        # Feature 2: usage_last_7_days_g
        date_map = usage.get(ingredient, {})
        last_7_total = 0.0

        for i in range(1, 8):
            d = (current_date - timedelta(days=i)).strftime("%Y-%m-%d")
            last_7_total += date_map.get(d, 0)

        # Feature 3: stock_to_threshold_ratio
        stock = row["current_stock_g"]
        threshold = row["threshold_g"]

        ratio = round(stock / threshold, 3) if threshold > 0 else 1.0

        # Feature 4: is_weekend
        is_weekend = 1 if current_date.weekday() >= 5 else 0

        enriched.append({
            **row,
            "days_since_last_used": days_since,
            "usage_last_7_days_g": round(last_7_total, 2),
            "stock_to_threshold_ratio": ratio,
            "is_weekend": is_weekend,
        })

    return enriched


def save_csv(rows):
    if not rows:
        print("ERROR: No rows to save.")
        return

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows → {OUTPUT_CSV}")


def main():
    print("Loading files...")
    logs, dishes, inventory, thresholds = load_files()

    print("\nRemoving duplicates...")
    logs = remove_duplicate_logs(logs)

    print("\nFlattening logs...")
    flat = flatten_logs(logs, dishes)

    print("\nBuilding usage...")
    usage = build_daily_usage(flat)

    print("\nBuilding base dataset...")
    rows = build_training_csv(usage, inventory, thresholds)

    print("\nAdding features...")
    rows = add_features(rows, usage)

    print("\nSaving CSV...")
    save_csv(rows)

    print("\nPreview:")
    for row in rows[:5]:
        print(row)


if __name__ == "__main__":
    main()