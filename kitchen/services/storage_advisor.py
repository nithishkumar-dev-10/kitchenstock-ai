STORAGE_RULES = {
    # Fridge items
    "chicken": "fridge",
    "fish": "fridge",
    "mutton": "fridge",
    "egg": "fridge",
    "milk": "fridge",
    "curd": "fridge",
    "butter": "fridge",
    "cheese": "fridge",
    "paneer": "fridge",
    "spinach": "fridge",
    "lettuce": "fridge",
    "mushroom": "fridge",
    "cucumber": "fridge",
    "carrot": "fridge",
    "beans": "fridge",
    "capsicum": "fridge",
    "cauliflower": "fridge",
    "cabbage": "fridge",
    "brinjal": "fridge",
    "tomato": "fridge",
    "coconut_milk": "fridge",
    "mayonnaise": "fridge",
    "bread": "fridge",

    # Room temperature items
    "rice": "room temperature",
    "basmati_rice": "room temperature",
    "flour": "room temperature",
    "toor_dal": "room temperature",
    "moong_dal": "room temperature",
    "oil": "room temperature",
    "onion": "room temperature",
    "potato": "room temperature",
    "garlic": "room temperature",
    "ginger": "room temperature",
    "sugar": "room temperature",
    "salt": "room temperature",
    "turmeric": "room temperature",
    "chili_powder": "room temperature",
    "cumin": "room temperature",
    "mustard_seeds": "room temperature",
    "noodles": "room temperature",
    "pasta": "room temperature",
    "oats": "room temperature",
}


def get_storage_advice(item: str) -> dict:
    storage = STORAGE_RULES.get(item.lower(), "room temperature")
    return {
        "item": item,
        "storage": storage,
        "tip": (
            "Keep refrigerated below 4°C" if storage == "fridge"
            else "Store in a cool, dry place away from sunlight"
        )
    }


def get_all_storage_advice(inventory: dict) -> list:
    return [get_storage_advice(item) for item in inventory.keys()]