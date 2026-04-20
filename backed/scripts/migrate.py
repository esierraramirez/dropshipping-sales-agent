"""
Script para aplicar migraciones a la base de datos
Ejecutar con: python -m scripts.migrate
"""
import sys
from pathlib import Path

# Agregar backed al path
backed_path = Path(__file__).parent.parent
sys.path.insert(0, str(backed_path))

from app.infrastructure.db.session import engine
from sqlalchemy import text

def run_migrations():
    """Ejecutar todas las migraciones SQL"""
    migrations_dir = Path(__file__).parent.parent / "migrations"
    
    if not migrations_dir.exists():
        print(f"❌ Directorio de migraciones no existe: {migrations_dir}")
        return False
    
    # Obtener todos los archivos .sql ordenados
    sql_files = sorted(migrations_dir.glob("*.sql"))
    
    if not sql_files:
        print("⚠️  No hay migraciones para ejecutar")
        return True
    
    with engine.connect() as conn:
        for sql_file in sql_files:
            print(f"\n📝 Aplicando: {sql_file.name}")
            
            try:
                sql_content = sql_file.read_text()
                conn.execute(text(sql_content))
                conn.commit()
                print(f"✅ {sql_file.name} aplicado exitosamente")
            except Exception as e:
                print(f"❌ Error en {sql_file.name}: {e}")
                conn.rollback()
                return False
    
    return True

if __name__ == "__main__":
    print("🔄 Iniciando migraciones...")
    success = run_migrations()
    
    if success:
        print("\n✅ Todas las migraciones se aplicaron correctamente")
        sys.exit(0)
    else:
        print("\n❌ Hubo errores durante las migraciones")
        sys.exit(1)
