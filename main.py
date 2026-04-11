from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from kitchen.core.config import settings
from api.routes import alerts, dishes, inventory, recipes, shopping,consumption
from kitchen.utils.exceptions import KitchenBaseError
from kitchen.utils.responses import error_response

app = FastAPI(title=settings.app_name,version=settings.version,debug=settings.debug)


@app.exception_handler(KitchenBaseError)
async def kitchen_exception_handler(request: Request, exc: KitchenBaseError):
    """Catch any unhandled KitchenBaseError and return a clean 500 response."""
    return JSONResponse(
        status_code=500,
        content=error_response(message=exc.message),
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Fallback for any truly unexpected errors."""
    return JSONResponse(
        status_code=500,
        content=error_response(message="An unexpected error occurred"),
    )



app.include_router(consumption.router, tags=["Consumption"])
app.include_router(alerts.router, tags=["Alerts"])
app.include_router(dishes.router, tags=["Dishes"])
app.include_router(inventory.router, tags=["Inventory"])
app.include_router(recipes.router, tags=["Recipes"])
app.include_router(shopping.router, tags=["Shopping"])


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name, "version": settings.version}