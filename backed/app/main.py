from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.infrastructure.db.session import Base, engine

# Importar modelos para que SQLAlchemy cree las tablas
from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.models.product import Product
from app.models.order import Order
from app.models.whatsapp_connection import WhatsAppConnection

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    """
    Lazy init: intentar crear tablas, pero no fallar si no hay conexión.
    Las tablas se crearán cuando el primer request necesite la BD.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tablas creadas/verificadas en Supabase")
    except Exception as e:
        print(f"⚠️  No se pudo conectar en startup: {type(e).__name__}")
        print("   Las tablas se crearán con el primer request")