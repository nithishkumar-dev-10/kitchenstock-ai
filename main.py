from fastapi import FastAPI
from api.routes import inventory
from api.routes import alerts
from api.routes import dishes
app=FastAPI()

app.include_router(inventory.router)
app.include_router(alerts.router)
app.include_router(dishes.router)
