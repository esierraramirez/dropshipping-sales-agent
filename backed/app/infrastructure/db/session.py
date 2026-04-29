from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings
from app.infrastructure.db.csv_audit import register_csv_audit_listeners


# Configurar SQLAlchemy para PostgreSQL con pooling
engine_kwargs = {
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
}

if "postgresql" in settings.DATABASE_URL:
    # Para Supabase Transaction Pooler (IPv4), no necesitamos SSL
    engine_kwargs["connect_args"] = {"sslmode": "prefer"}

engine = create_engine(settings.DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


register_csv_audit_listeners(SessionLocal, Base)


# Flag para lazy init de tablas
_tables_initialized = False


def get_db():
    global _tables_initialized
    
    # Crear tablas una sola vez en el primer acceso (SIN eliminar datos existentes)
    if not _tables_initialized:
        try:
            # Crear todas las tablas si no existen (NO ELIMINAR NUNCA)
            Base.metadata.create_all(bind=engine)
            _tables_initialized = True
            print("✅ Tablas creadas/verificadas en Supabase (datos preservados)")
        except Exception as e:
            print(f"⚠️  Error al crear tablas: {type(e).__name__}: {e}")
            # Marcar como inicializado anyway para no intentar de nuevo
            _tables_initialized = True
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()