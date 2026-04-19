#!/usr/bin/env python3
"""
🚀 Migración: Agregar columna phone_number a tabla whatsapp_connections

Este script agrega el campo phone_number (número formateado +52 1 55...)
a la tabla whatsapp_connections para cada empresa.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

# Agregar ruta del directorio backed
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.core.config import settings

def get_connection_string():
    """Construir conexión a PostgreSQL"""
    return (
        f"postgresql://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )

def migrate_whatsapp_phone_number():
    """Agregar columna phone_number a whatsapp_connections"""
    
    db_url = get_connection_string()
    engine = create_engine(db_url, echo=False)
    
    print("🚀 Starting database migration...")
    print(f"📍 Connecting to: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # Verificar si la columna ya existe
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('whatsapp_connections')]
        
        if 'phone_number' in columns:
            print("✅ Columna 'phone_number' ya existe en la tabla.")
            return
        
        # Agregar la columna
        with engine.begin() as conn:
            try:
                conn.execute(text("""
                    ALTER TABLE whatsapp_connections 
                    ADD COLUMN phone_number VARCHAR(20) NULL;
                """))
                print("✅ Columna 'phone_number' agregada exitosamente")
                print("   - Tipo: VARCHAR(20)")
                print("   - Nullable: True (puede ser NULL)")
                print("   - Formato esperado: +52 1 55 XXXX XXXX")
                
            except Exception as e:
                print(f"❌ Error al agregar columna: {str(e)}")
                raise
        
        print("\n✅ Migration completed successfully!")
        print("📋 Resumen:")
        print("   ✓ Tabla: whatsapp_connections")
        print("   ✓ Nueva columna: phone_number (VARCHAR 20)")
        print("   ✓ Estado: Aplicada")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    migrate_whatsapp_phone_number()
