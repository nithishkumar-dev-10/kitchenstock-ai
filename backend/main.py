from fastapi import FastAPI
from backend.routes.ingredient import router
app=FastAPI()
app.include_router(router)

@app.get('/')
def home():
    return {"msg":"Kitchen AI is running"}