#!/usr/bin/env python
"""Setup PostgreSQL database for the application."""

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Intentar múltiples configuraciones de contraseña
passwords_to_try = ["", "postgres", "123456", "1234", "admin"]

postgres_config = None
connection = None

for pwd in passwords_to_try:
    try:
        test_config = {
            "user": "postgres",
            "password": pwd,
            "host": "localhost",
            "port": "5432",
            "database": "postgres"
        }
        conn = psycopg2.connect(**test_config)
        print(f"✓ Conectado a PostgreSQL con contraseña: {'(vacía)' if pwd == '' else pwd}")
        postgres_config = test_config
        connection = conn
        break
    except psycopg2.Error:
        continue

if not postgres_config:
    print("✗ No se pudo conectar a PostgreSQL. Verifique que el servidor esté corriendo.")
    print("Intentó con contraseñas:", passwords_to_try)
    exit(1)

database_name = "dropshipping_db"

try:
    # Conectarse a PostgreSQL
    connection = psycopg2.connect(**postgres_config)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    
    # Intentar crear la base de datos
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
    print(f"✓ Base de datos '{database_name}' creada exitosamente")
    
except psycopg2.Error as error:
    if "already exists" in str(error):
        print(f"✓ Base de datos '{database_name}' ya existe")
    else:
        print(f"✗ Error: {error}")
finally:
    if connection:
        cursor.close()
        connection.close()

# Ahora crear las tablas
print("\nCreando tablas...")
from app.infrastructure.db.session import Base, engine

try:
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente")
except Exception as e:
    print(f"✗ Error al crear tablas: {e}")
