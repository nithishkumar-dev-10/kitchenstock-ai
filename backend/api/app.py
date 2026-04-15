from fastapi import FastAPI

app = FastAPI(title="KitchenStock AI")

@app.get("/health")
def health():
    return {"status": "ok"}