#!/usr/bin/env python3
"""Prueba end-to-end para verificar si la cuenta de Akari crea una orden en la base de datos tras una conversación."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

BACKED_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKED_DIR.parent
os.chdir(BACKED_DIR)
sys.path.insert(0, str(BACKED_DIR))

from app.core.config import settings
from app.infrastructure.db.session import Base
from app.models.order import Order
from app.models.product import Product
from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.models.whatsapp_connection import WhatsAppConnection
from app.models.audit_log import AuditLog


DEFAULT_BASE_URL = os.getenv("AKARI_TEST_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_EMAIL = os.getenv("AKARI_TEST_EMAIL", "akari@gmail.com")
DEFAULT_PASSWORD = os.getenv("AKARI_TEST_PASSWORD", "akari123")


@dataclass
class ConversationStep:
    message: str
    purchase_context: dict[str, Any] | None = None


def build_conversation() -> list[ConversationStep]:
    """Conversación corta orientada a disparar la creación de una orden."""
    return [
        ConversationStep("hola"),
        ConversationStep(
            "Me interesa el producto y quiero comprarlo",
            purchase_context={
                "customer_name": "Juan Perez",
                "customer_phone": "3001234567",
                "customer_address": "Calle 1 #2-3",
                "items": [
                    {
                        "product_id": "SKU-001",
                        "product_name": "Audífonos Inalámbricos",
                        "quantity": 1,
                        "unit_price": 249900,
                    }
                ],
                "total_amount": 249900,
                "is_confirmed": True,
            },
        ),
        ConversationStep("ok"),
    ]


def create_session() -> sessionmaker:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)


def fetch_current_order_count(db_session) -> int:
    return db_session.query(Order).count()


def login(base_url: str, email: str, password: str) -> tuple[str, dict[str, Any]]:
    response = requests.post(
        f"{base_url}/auth/login",
        json={"email": email, "password": password},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    token = payload["access_token"]
    return token, payload["vendor"]


def chat(base_url: str, token: str, message: str, purchase_context: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    payload: dict[str, Any] = {
        "message": message,
        "history": [],
    }
    if purchase_context is not None:
        payload["purchase_context"] = purchase_context

    response = requests.post(
        f"{base_url}/chat/me",
        json=payload,
        headers=headers,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def find_latest_order(db_session, vendor_id: int) -> Order | None:
    stmt = select(Order).where(Order.vendor_id == vendor_id).order_by(Order.id.desc())
    return db_session.execute(stmt).scalars().first()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--email", default=DEFAULT_EMAIL)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    args = parser.parse_args()

    session_factory = create_session()
    db = session_factory()

    print("=== PRUEBA AKARI: CREACION DE ORDEN DESPUES DE CONVERSACION ===")
    before_count = fetch_current_order_count(db)
    print(f"Ordenes antes de la prueba: {before_count}")

    token, vendor_data = login(args.base_url, args.email, args.password)
    vendor_id = int(vendor_data["id"])
    vendor_name = vendor_data["name"]
    print(f"Sesion iniciada para: {vendor_name} ({args.email})")

    last_response: dict[str, Any] | None = None
    for step in build_conversation():
        last_response = chat(
            base_url=args.base_url,
            token=token,
            message=step.message,
            purchase_context=step.purchase_context,
        )
        print(f"Mensaje: {step.message}")
        print(f"Respuesta: {last_response.get('agent_response', '')}")
        if last_response.get("order_created"):
            print(f"Orden creada en respuesta: {json.dumps(last_response['order_created'], ensure_ascii=False)}")

    after_count = fetch_current_order_count(db)
    latest_order = find_latest_order(db, vendor_id)

    print("\n=== RESULTADO ===")
    print(f"Ordenes despues de la prueba: {after_count}")
    print(f"Nuevas ordenes creadas: {after_count - before_count}")

    if latest_order:
        print("\nUltima orden registrada:")
        print(f"  ID: {latest_order.id}")
        print(f"  Cliente: {latest_order.customer_name}")
        print(f"  Telefono: {latest_order.customer_phone}")
        print(f"  Direccion: {latest_order.customer_address}")
        print(f"  Total: {latest_order.total_amount}")
        print(f"  Estado: {latest_order.status}")
        print(f"  Resumen: {latest_order.chat_summary}")

    if after_count <= before_count:
        print("\nNO SE CREO NINGUNA ORDEN NUEVA.")
        return 1

    print("\nSI SE CREO UNA ORDEN NUEVA EN LA BASE DE DATOS.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())