from fastapi import FastAPI
from api.routes import inventory
from api.routes import alerts
from api.routes import dishes
from api.routes import recipes
from api.routes import shopping

app=FastAPI()

app.include_router(inventory.router)
app.include_router(alerts.router)
app.include_router(dishes.router)
app.include_router(recipes.router)
app.include_router(shopping.router)
