from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from kitchen.core.config import settings
from kitchen.utils.exceptions import KitchenBaseError, NoDataAvailableError
from kitchen.utils.responses import error_response

from fastapi.middleware.cors import CORSMiddleware


# Routers
from api.routes import (
    alerts,
    dishes,
    inventory,
    recipes,
    shopping,
    consumption,
    prediction,
    storage,
)

# Services
from kitchen.services.prediction_engine import predict_runout
from kitchen.services.alert_system import check_alerts

# OPTIONAL (future ML integration)
try:
    from kitchen.services.ml_engine import predict_with_model
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


# ------------------ APP INIT ------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------ EXCEPTION HANDLERS ------------------

@app.exception_handler(KitchenBaseError)
async def kitchen_exception_handler(request: Request, exc: KitchenBaseError):
    return JSONResponse(
        status_code=500,
        content=error_response(message=exc.message),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response(message="An unexpected error occurred"),
    )


# ------------------ CORE DASHBOARD ------------------

@app.get("/dashboard", tags=["Dashboard"])
def dashboard():
    """
    Dashboard combines:
    - predictions (ML or fallback)
    - alerts
    """

    #  Prediction logic (ML + fallback)
    try:
        if ML_AVAILABLE:
            predictions = predict_with_model()
        else:
            predictions = predict_runout()
    except NoDataAvailableError:
        predictions = {"predictions": []}
    except Exception:
        # fallback safety
        predictions = predict_runout()

    # 🔥 Alerts
    try:
        alerts_data = check_alerts()
    except Exception:
        alerts_data = []

    return {
        "predictions": predictions,
        "alerts": alerts_data
    }


# ------------------ ROUTERS ------------------

app.include_router(storage.router, tags=["Storage"])
app.include_router(prediction.router, tags=["Prediction"])
app.include_router(consumption.router, tags=["Consumption"])
app.include_router(alerts.router, tags=["Alerts"])
app.include_router(dishes.router, tags=["Dishes"])
app.include_router(inventory.router,tags=["Inventory"])
app.include_router(recipes.router,tags=["Recipes"])
app.include_router(shopping.router, tags=["Shopping"])


# ------------------ HEALTH CHECK ------------------

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.version,
        "ml_enabled": ML_AVAILABLE   #  NEW
    }