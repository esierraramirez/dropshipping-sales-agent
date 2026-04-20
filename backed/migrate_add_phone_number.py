"""
Script para migrar y agregar la columna phone_number a la tabla whatsapp_connections
"""
import os
from sqlalchemy import create_engine, text

# Obtener la URL de la BD de Supabase
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Negritomotero%24123@db.zywqomqbvxuwbksigcmp.supabase.co:5432/postgres",
)

def migrate():
    """Ejecuta la migración para agregar phone_number"""
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as connection:
            # Verificar si la columna ya existe
            result = connection.execute(
                text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name='whatsapp_connections' AND column_name='phone_number'
                """)
            )
            
            if result.fetchone():
                print("✅ La columna 'phone_number' ya existe")
                return
            
            # Agregar la columna
            print("⏳ Agregando columna phone_number...")
            connection.execute(
                text("""
                    ALTER TABLE whatsapp_connections 
                    ADD COLUMN phone_number VARCHAR(20) DEFAULT NULL
                """)
            )
            connection.commit()
            print("✅ Columna phone_number agregada exitosamente")
            
    except Exception as e:
        print(f"❌ Error en la migración: {e}")

if __name__ == "__main__":
    migrate()
