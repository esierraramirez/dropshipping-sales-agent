import psycopg2
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
db_url = os.getenv('DATABASE_URL')
parsed = urlparse(db_url)

print("=" * 50)
print("TEST DE CONEXION A SUPABASE")
print("=" * 50)
print(f"\nHost: {parsed.hostname}")
print(f"Port: {parsed.port}")
print(f"User: {parsed.username}")
print(f"DB: {parsed.path.lstrip('/')}")

try:
    print("\nIntentando conexion con timeout=10s...")
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip('/'),
        sslmode='require',
        connect_timeout=10
    )
    print("\n✅ ¡CONECTADO A SUPABASE EXITOSAMENTE!")
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"Versión: {version[0][:60]}")
    cursor.close()
    conn.close()
except psycopg2.Error as e:
    print(f"\n❌ Error de PostgreSQL: {e}")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Tipo: {type(e).__name__}")
    print("\n💡 CAUSA PROBABLE: DNS no puede resolver db.zywqomqbvxuwbksigcmp.supabase.co")
    print("\n🔧 SOLUCIONES:")
    print("  1. Verifica conexión a internet: ping google.com")
    print("  2. Prueba con DNS de Google:")
    print("     nslookup db.zywqomqbvxuwbksigcmp.supabase.co 8.8.8.8")
    print("  3. Si funciona, cambia DNS de tu PC a 8.8.8.8")
