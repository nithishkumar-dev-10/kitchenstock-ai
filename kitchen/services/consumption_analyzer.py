from collections import defaultdict
from datetime import datetime
from kitchen.services.data_loader import load_dishes
import json


class ConsumptionAnalyzer:
    def __init__(self):
        self.consumption_log = self.load_consumption_log()
        self.dishes = load_dishes()

    def get_ingredient_usage(self):
        """
        Convert dish logs → ingredient usage list
        """
        usage_data = []

        for log in self.consumption_log:
            dish_name = log.get("dish")
            date = log.get("date")

            if dish_name not in self.dishes:
                continue

            ingredients = self.dishes[dish_name]

            for ingredient, qty in ingredients.items():
                usage_data.append({
                    "ingredient": ingredient,
                    "usage": qty,
                    "date": date
                })

        return usage_data

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

            total_usage[ingredient] += usage
            dates.add(date)

        num_days = len(dates) if dates else 1

        daily_usage = {}

        for ingredient, total in total_usage.items():
            daily_usage[ingredient] = round(total / num_days, 2)

        return daily_usage

    def get_usage_for_ingredient(self, ingredient_name):
        """
        Get daily usage for a single ingredient
        """
        daily_usage = self.get_daily_usage()
        return daily_usage.get(ingredient_name, 0)
    
    def load_consumption_log(self):
        try:
            with open("data/consumption_log.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return []