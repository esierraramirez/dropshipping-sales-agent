#!/usr/bin/env python
"""Test import app.main"""
import sys
import traceback

print("=" * 60)
print("DIAGNOSTICO DE IMPORTACION")
print("=" * 60)

print(f"\nPython: {sys.version}")
print(f"Path: {sys.path[:3]}")

try:
    print("\n[1/3] Importando FastAPI...")
    from fastapi import FastAPI
    print("✅ FastAPI OK")
    
    print("[2/3] Importando app.core.config...")
    from app.core.config import settings
    print("✅ app.core.config OK")
    
    print("[3/3] Importando app.main...")
    from app.main import app
    print("✅ app.main OK")
    
    print("\n" + "=" * 60)
    print("✅ ¡TODOS LOS IMPORTS FUNCIONAN!")
    print("=" * 60)
    
except ImportError as e:
    print(f"\n❌ ImportError: {e}")
    traceback.print_exc()
    sys.exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
    traceback.print_exc()
    sys.exit(1)
