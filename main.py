from fastapi import FastAPI
from api.routes import inventory

app=FastAPI()

app.include_router(inventory.router)
