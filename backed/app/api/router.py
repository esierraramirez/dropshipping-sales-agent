from fastapi import APIRouter
from app.api.routes.health_routes import router as health_router
from app.api.routes.catalog_routes import router as catalog_router
from app.api.routes.vendor_routes import router as vendor_router
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.settings_routes import router as settings_router
from app.api.routes.llm_routes import router as llm_router
from app.api.routes.retrieval_routes import router as retrieval_router
from app.api.routes.chat_routes import router as chat_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(settings_router, tags=["settings"])
api_router.include_router(llm_router, tags=["llm"])
api_router.include_router(retrieval_router, tags=["retrieval"])
api_router.include_router(chat_router, tags=["chat"])
api_router.include_router(catalog_router, tags=["catalog"])
api_router.include_router(vendor_router, tags=["vendors"])
