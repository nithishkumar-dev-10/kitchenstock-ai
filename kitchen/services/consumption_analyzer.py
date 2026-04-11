from collections import defaultdict
from datetime import datetime, timedelta
from kitchen.services.data_loader import load_dishes, load_inventory, save_inventory
import json


class ConsumptionAnalyzer:
    def __init__(self):
        self.consumption_log = self.load_consumption_log()
        self.dishes = load_dishes()

    # ------------------ LOAD LOG ------------------
    def load_consumption_log(self):
        try:
            with open("data/consumption_log.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    # ------------------ INGREDIENT USAGE ------------------
    def get_ingredient_usage(self):
        """
        Convert dish logs → ingredient usage list (FIXED)
        """
        usage_data = []

        for log in self.consumption_log:
            dish_name = log.get("dish")
            servings = log.get("servings", 1)   # ✅ FIX
            date = log.get("date")

            if dish_name not in self.dishes:
                continue

            ingredients = self.dishes[dish_name]

            for ingredient, qty in ingredients.items():
                usage_data.append({
                    "ingredient": ingredient,
                    "usage": qty * servings,   # ✅ FIX (VERY IMPORTANT)
                    "date": date
                })

        return usage_data

    # ------------------ DAILY USAGE ------------------
    def get_daily_usage(self):
        """
        Calculate average daily usage for each ingredient
        """
        usage_data = self.get_ingredient_usage()

        total_usage = defaultdict(int)
        dates = set()

        for entry in usage_data:
            ingredient = entry["ingredient"]
            usage = entry["usage"]
            date = entry["date"]

            # ✅ SAFETY FIX
            if isinstance(usage, (int, float)):
                total_usage[ingredient] += usage

            if date:
                dates.add(date)

        num_days = len(dates) if dates else 1

        daily_usage = {}

        for ingredient, total in total_usage.items():
            daily_usage[ingredient] = round(total / num_days, 2)

        return daily_usage

    # ------------------ SINGLE ITEM USAGE ------------------
    def get_usage_for_ingredient(self, ingredient_name):
        daily_usage = self.get_daily_usage()
        return daily_usage.get(ingredient_name, 0)

    # ------------------ LOG DISH ------------------
    def log_dish(self, dish_name: str, servings: int, date: str) -> dict:
        """
        Log a dish + deduct inventory
        """
        if servings <= 0:
            raise ValueError("Servings must be greater than 0")

        if dish_name not in self.dishes:
            raise ValueError(f"Dish '{dish_name}' not found in dishes.json")

        new_entry = {
            "dish": dish_name,
            "servings": servings,
            "date": date
        }

        self.consumption_log.append(new_entry)

        with open("data/consumption_log.json", "w") as f:
            json.dump(self.consumption_log, f, indent=2)

        # ------------------ INVENTORY DEDUCTION ------------------
        inventory = load_inventory()
        ingredients = self.dishes[dish_name]

        deducted = []
        skipped = []

        for item, qty_per_serving in ingredients.items():
            required = qty_per_serving * servings

            if item in inventory:
                inventory[item]["quantity"] = max(
                    0,
                    inventory[item]["quantity"] - required
                )
                deducted.append({"item": item, "deducted": required})
            else:
                skipped.append(item)

        save_inventory(inventory)

        return {
            "logged": True,
            "dish": dish_name,
            "servings": servings,
            "date": date,
            "inventory_deducted": deducted,
            "ingredients_not_in_inventory": skipped
        }

    # ------------------ MISSING DAYS ------------------
    def estimate_missing_days(self, from_date: str, to_date: str) -> dict:
        start = datetime.strptime(from_date, "%Y-%m-%d")
        end = datetime.strptime(to_date, "%Y-%m-%d")

        logged_dates = set(entry["date"] for entry in self.consumption_log)

        missing_dates = []
        current = start

        while current <= end:
            date_str = current.strftime("%Y-%m-%d")
            if date_str not in logged_dates:
                missing_dates.append(date_str)
            current += timedelta(days=1)

        if not missing_dates:
            return {
                "missing_days": 0,
                "estimated_usage": {},
                "message": "No missing days found"
            }

        daily_usage = self.get_daily_usage()

        estimated_usage = {}
        for ingredient, usage_per_day in daily_usage.items():
            estimated_usage[ingredient] = round(
                usage_per_day * len(missing_dates), 2
            )

        return {
            "missing_days": len(missing_dates),
            "missing_dates": missing_dates,
            "estimated_usage": estimated_usage,
            "message": f"Estimated usage for {len(missing_dates)} unlogged day(s)"
        }