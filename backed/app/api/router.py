from fastapi import APIRouter
from app.api.routes.health_routes import router as health_router
from app.api.routes.catalog_routes import router as catalog_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(catalog_router, tags=["catalog"])