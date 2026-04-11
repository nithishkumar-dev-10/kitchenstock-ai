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

# ── File paths ────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent.parent
LOG_FILE      = ROOT / "data" / "consumption_log.json"
DISHES_FILE   = ROOT / "data" / "dishes.json"
INVENTORY_FILE= ROOT / "data" / "inventory.json"
THRESHOLD_FILE= ROOT / "data" / "thresholds.json"
OUTPUT_CSV    = ROOT / "data" / "training_data.csv"

# ── Step A: Unit conversion table (count → grams) ─────────
COUNT_TO_GRAMS = {
    "egg":    60,    # 1 egg ≈ 60g
    "bread":  30,    # 1 slice ≈ 30g
    "banana": 120,   # 1 banana ≈ 120g
    "apple":  180,   # 1 apple ≈ 180g
    "orange": 150,   # 1 orange ≈ 150g
    "mango":  200,   # 1 mango ≈ 200g
    "lemon":  60,    # 1 lemon ≈ 60g
}


def load_files():
    """Load all 4 JSON files."""
    logs      = json.loads(LOG_FILE.read_text())
    dishes    = json.loads(DISHES_FILE.read_text())
    inventory = json.loads(INVENTORY_FILE.read_text())
    thresholds= json.loads(THRESHOLD_FILE.read_text())
    return logs, dishes, inventory, thresholds


def convert_to_grams(ingredient, quantity):
    """
    Step A: Convert count-based items to grams.
    If item is already in grams, return as-is.
    """
    if ingredient in COUNT_TO_GRAMS:
        return quantity * COUNT_TO_GRAMS[ingredient]
    return quantity


def remove_duplicate_logs(logs):
    """
    Step D: Remove duplicate dish+date entries.
    Keep only the first occurrence.
    """
    seen = set()
    clean_logs = []
    for entry in logs:
        key = (entry["dish"], entry["date"])
        if key not in seen:
            seen.add(key)
            clean_logs.append(entry)
    return clean_logs


def flatten_logs(logs, dishes):
    """
    Step C: Expand each log entry into ingredient-level usage.

    Input:  [{dish: "idli", servings: 2, date: "2026-03-01"}, ...]
    Output: [{date: "2026-03-01", ingredient: "idli_rice", used_g: 400}, ...]
    """
    flat = []

    for entry in logs:
        dish_name = entry["dish"]
        servings  = entry["servings"]
        date      = entry["date"]

        # Skip if dish not in dishes.json (safety check)
        if dish_name not in dishes:
            print(f"  WARNING: '{dish_name}' not in dishes.json — skipping")
            continue

        for ingredient, qty_per_serving in dishes[dish_name].items():
            # Step B: Skip the 'steps' key (cooking instructions, not food)
            if ingredient == "steps":
                continue

            # Multiply by servings to get total used
            total_used = qty_per_serving * servings

            # Step A: Convert count → grams
            total_used_g = convert_to_grams(ingredient, total_used)

            flat.append({
                "date":       date,
                "ingredient": ingredient,
                "used_g":     round(total_used_g, 2)
            })

    return flat


def build_daily_usage(flat_logs):
    """
    Aggregate flat log entries by ingredient+date.
    (An ingredient can appear multiple times in one day from different dishes)

    Returns: {ingredient: {date: total_used_g}}
    """
    usage = defaultdict(lambda: defaultdict(float))

    for entry in flat_logs:
        ingredient = entry["ingredient"]
        date       = entry["date"]
        used_g     = entry["used_g"]
        usage[ingredient][date] += used_g

    return usage


def build_training_csv(usage, inventory, thresholds):
    """
    Step E: Build one row per ingredient per date.

    Each row contains:
      date, ingredient, used_g (that day),
      current_stock_g, threshold_g, avg_daily_usage_g
    """
    rows = []

    all_dates = sorted({
        date
        for date_map in usage.values()
        for date in date_map
    })

    for ingredient, date_map in usage.items():

        # Get stock in grams (convert if count-based)
        inv_data     = inventory.get(ingredient, {})
        raw_stock    = inv_data.get("quantity", 0)
        stock_g      = convert_to_grams(ingredient, raw_stock)

        # Get threshold in grams
        raw_threshold = thresholds.get(ingredient, 0)
        threshold_g   = convert_to_grams(ingredient, raw_threshold)

        # Compute average daily usage across all logged days
        total_used    = sum(date_map.values())
        num_days      = len(all_dates)
        avg_daily_g   = round(total_used / num_days, 2)

        # Compute days until runout (cap at 90 — beyond 90 is "plenty")
        if avg_daily_g > 0:
            days_until_runout = round(stock_g / avg_daily_g, 1)
            days_until_runout = min(days_until_runout, 90)  # cap at 90
        else:
            days_until_runout = 90  # not used = no runout risk

        for date in all_dates:
            used_today = round(date_map.get(date, 0), 2)

            rows.append({
                "date":              date,
                "ingredient":        ingredient,
                "used_g":            used_today,
                "current_stock_g":   round(stock_g, 2),
                "threshold_g":       round(threshold_g, 2),
                "avg_daily_usage_g": avg_daily_g,
                "days_until_runout": days_until_runout,  # ← ML label
            })

    return rows


def save_csv(rows):
    """Save rows to data/training_data.csv"""
    if not rows:
        print("ERROR: No rows to save.")
        return

    fieldnames = rows[0].keys()
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Saved {len(rows)} rows → {OUTPUT_CSV}")


def main():
    print("Loading files...")
    logs, dishes, inventory, thresholds = load_files()
    print(f"  Logs: {len(logs)} entries")
    print(f"  Dishes: {len(dishes)} dishes")
    print(f"  Inventory: {len(inventory)} items")
    print(f"  Thresholds: {len(thresholds)} items")

    print("\nRemoving duplicates...")
    logs = remove_duplicate_logs(logs)
    print(f"  Clean logs: {len(logs)} entries")

    print("\nFlattening logs into ingredient-level usage...")
    flat = flatten_logs(logs, dishes)
    print(f"  Flat entries: {len(flat)}")

    print("\nAggregating daily usage per ingredient...")
    usage = build_daily_usage(flat)
    print(f"  Unique ingredients tracked: {len(usage)}")

    print("\nBuilding training rows...")
    rows = build_training_csv(usage, inventory, thresholds)
    print(f"  Total rows: {len(rows)}")

    print("\nSaving CSV...")
    save_csv(rows)

    print("\nDone. Preview of first 5 rows:")
    for row in rows[:5]:
        print(f"  {row}")


if __name__ == "__main__":
    main()