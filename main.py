from kitchen.services.dish_checker import check_ingredients
from kitchen.services.dish_engine import cook_dish
from kitchen.services.inventory_manager import add_stock, print_inventory
from kitchen.services.alert_system import check_alerts
from kitchen.services.shopping_list import generate_shopping_list
from kitchen.services.recipe_suggester import suggest_recipes



# Add stock 
add_stock("wheat", 2, "kg")

# Show inventory
print_inventory()

# Check if dish can be cooked
check_ingredients("fried_rice", 2)

# Cook dish
cook_dish("fried_rice", 1)

# Alert system
check_alerts()

# Shopping List
generate_shopping_list()

# Recipe Suggestion
suggest_recipes()