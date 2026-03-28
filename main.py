from kitchen.services.dish_checker import check_ingredients
from kitchen.services.dish_engine import cook_dish

# Step 1: Check
check_ingredients("fried_rice", 2)

# Step 2: Cook
cook_dish("fried_rice", 1)