from kitchen.services.dish_checker import check_ingredients
from kitchen.services.dish_engine import cook_dish
from kitchen.services.inventory_manager import add_stock, print_inventory


# Add stock (simulate buying)
add_stock("wheat", 2, "kg")

# Show inventory
print_inventory()

# Check if dish can be cooked
check_ingredients("fried_rice", 2)

# Cook dish
cook_dish("fried_rice", 2)