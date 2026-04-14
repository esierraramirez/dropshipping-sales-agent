from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


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


# Flag para lazy init de tablas
_tables_initialized = False


def get_db():
    global _tables_initialized
    
    # Crear tablas una sola vez en el primer acceso
    if not _tables_initialized:
        try:
            # Para PostgreSQL: ejecutar DROP CASCADE para limpiar vistas y dependencias
            if "postgresql" in settings.DATABASE_URL:
                from sqlalchemy import text
                with engine.connect() as conn:
                    # Listar todas las vistas y tablas y eliminarlas con CASCADE
                    drop_views_sql = """
                    DROP VIEW IF EXISTS dashboard_overview CASCADE;
                    DROP TABLE IF EXISTS whatsapp_connections CASCADE;
                    DROP TABLE IF EXISTS conversations CASCADE;
                    DROP TABLE IF EXISTS knowledge_base CASCADE;
                    DROP TABLE IF EXISTS orders CASCADE;
                    DROP TABLE IF EXISTS products CASCADE;
                    DROP TABLE IF EXISTS vendor_settings CASCADE;
                    DROP TABLE IF EXISTS whatsapp_connections CASCADE;
                    DROP TABLE IF EXISTS vendors CASCADE;
                    """
                    conn.execute(text(drop_views_sql))
                    conn.commit()
                    print("🔄 Vistas y tablas eliminadas")
            else:
                Base.metadata.drop_all(bind=engine)
                print("🔄 Tablas eliminadas")
            
            # Luego crear las tablas con el esquema correcto
            Base.metadata.create_all(bind=engine)
            _tables_initialized = True
            print("✅ Tablas recreadas/verificadas en Supabase")
        except Exception as e:
            print(f"⚠️  Error al recrear tablas: {type(e).__name__}: {e}")
            # Marcar como inicializado anyway para no intentar de nuevo
            _tables_initialized = True
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()