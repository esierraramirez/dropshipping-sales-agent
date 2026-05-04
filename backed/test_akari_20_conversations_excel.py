#!/usr/bin/env python3
"""Prueba end-to-end de 20 conversaciones con la cuenta de Akari y exportacion a Excel."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BACKED_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKED_DIR.parent
OUTPUT_DIR = ROOT_DIR / "data" / "reports"
OUTPUT_FILE = OUTPUT_DIR / "akari_20_conversations_order_test.xlsx"

os.chdir(BACKED_DIR)
sys.path.insert(0, str(BACKED_DIR))

from app.core.config import settings
from app.infrastructure.db.session import Base
from app.models.audit_log import AuditLog
from app.models.order import Order
from app.models.product import Product
from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.models.whatsapp_connection import WhatsAppConnection


DEFAULT_BASE_URL = os.getenv("AKARI_TEST_BASE_URL", "http://127.0.0.1:8000")
DEFAULT_EMAIL = os.getenv("AKARI_TEST_EMAIL", "akari@gmail.com")
DEFAULT_PASSWORD = os.getenv("AKARI_TEST_PASSWORD", "akari123")


@dataclass
class ConversationScenario:
    scenario_id: int
    product_name: str
    product_id: str
    unit_price: float
    customer_name: str
    customer_phone: str
    customer_address: str
    question_1: str
    question_2: str
    question_3: str
    confirmation_message: str


@dataclass
class ConversationStep:
    step_number: int
    message: str
    purchase_context: dict[str, Any] | None = None


PRODUCT_POOL = [
    ("SKU-001", "Audífonos Inalámbricos", 249900.0),
    ("SKU-002", "Zapatillas Running", 189900.0),
    ("SKU-003", "Producto de prueba", 65000.0),
    ("SKU-004", "Mochila Impermeable", 129900.0),
    ("SKU-005", "Lámpara LED RGB", 89900.0),
    ("SKU-006", "Camisa Oxford Blanca Essential", 159900.0),
    ("SKU-007", "Pantalón Palazzo Brisa", 179900.0),
    ("SKU-008", "Saco Tejido Andino", 149900.0),
    ("SKU-009", "Abrigo Largo Lana Nórdica", 229900.0),
    ("SKU-010", "Bolso Urbano Minimal", 119900.0),
]

QUESTIONS = [
    "¿Tienen disponibilidad de este producto?",
    "¿Qué me puedes decir de sus características?",
    "¿Hay otras opciones parecidas?",
    "Perfecto, lo quiero comprar y confirmo la orden.",
]


def build_scenarios() -> list[ConversationScenario]:
    scenarios: list[ConversationScenario] = []
    for idx in range(20):
        product_id, product_name, unit_price = PRODUCT_POOL[idx % len(PRODUCT_POOL)]
        scenarios.append(
            ConversationScenario(
                scenario_id=idx + 1,
                product_name=product_name,
                product_id=product_id,
                unit_price=unit_price,
                customer_name=f"Cliente Akari {idx + 1}",
                customer_phone=f"300555{1000 + idx}",
                customer_address=f"Calle {idx + 1} #12-{idx + 3}, Medellin",
                question_1=f"Hola, quiero saber si tienen {product_name.lower()}.",
                question_2=f"¿Cuanto cuesta el {product_name.lower()}?",
                question_3=f"¿Me recomiendas algo similar al {product_name.lower()}?",
                confirmation_message=QUESTIONS[3],
            )
        )
    return scenarios


def create_session() -> sessionmaker:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)


def fetch_current_order_count(db_session) -> int:
    return db_session.query(Order).count()


def find_latest_order(db_session, vendor_id: int) -> Order | None:
    return (
        db_session.query(Order)
        .filter(Order.vendor_id == vendor_id)
        .order_by(Order.id.desc())
        .first()
    )


def login(base_url: str, email: str, password: str) -> tuple[str, dict[str, Any]]:
    response = requests.post(
        f"{base_url}/auth/login",
        json={"email": email, "password": password},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["access_token"], payload["vendor"]


def chat(
    base_url: str,
    token: str,
    message: str,
    history: list[dict[str, str]],
    purchase_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    headers = {"Authorization": f"Bearer {token}"}
    payload: dict[str, Any] = {
        "message": message,
        "history": history,
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


def build_purchase_context(scenario: ConversationScenario) -> dict[str, Any]:
    return {
        "customer_name": scenario.customer_name,
        "customer_phone": scenario.customer_phone,
        "customer_address": scenario.customer_address,
        "items": [
            {
                "product_id": scenario.product_id,
                "product_name": scenario.product_name,
                "quantity": 1,
                "unit_price": scenario.unit_price,
            }
        ],
        "total_amount": scenario.unit_price,
        "is_confirmed": True,
    }


def build_steps(scenario: ConversationScenario) -> list[ConversationStep]:
    return [
        ConversationStep(1, scenario.question_1),
        ConversationStep(2, scenario.question_2),
        ConversationStep(3, scenario.question_3),
        ConversationStep(4, scenario.confirmation_message, build_purchase_context(scenario)),
    ]


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--email", default=DEFAULT_EMAIL)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--output", default=str(OUTPUT_FILE))
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    session_factory = create_session()
    db = session_factory()

    print("=== AKARI 20 CONVERSACIONES / ORDENES ===")
    before_count = fetch_current_order_count(db)
    print(f"Ordenes antes: {before_count}")

    token, vendor_data = login(args.base_url, args.email, args.password)
    vendor_id = int(vendor_data["id"])
    vendor_name = vendor_data["name"]
    print(f"Sesion iniciada para: {vendor_name} ({args.email})")

    scenarios = build_scenarios()
    detail_rows: list[dict[str, Any]] = []
    order_rows: list[dict[str, Any]] = []

    for scenario in scenarios:
        history: list[dict[str, str]] = []
        last_response: dict[str, Any] | None = None
        order_created_at_step = None

        print(f"\n--- Conversacion {scenario.scenario_id}: {scenario.product_name} ---")
        for step in build_steps(scenario):
            response = chat(
                base_url=args.base_url,
                token=token,
                message=step.message,
                history=history,
                purchase_context=step.purchase_context,
            )
            last_response = response

            detail_rows.append(
                {
                    "scenario_id": scenario.scenario_id,
                    "step_number": step.step_number,
                    "customer_name": scenario.customer_name,
                    "product_name": scenario.product_name,
                    "product_id": scenario.product_id,
                    "message": step.message,
                    "agent_response": normalize_text(response.get("agent_response")),
                    "order_created": bool(response.get("order_created")),
                    "matches_found": response.get("matches_found", 0),
                    "purchase_context": json.dumps(response.get("purchase_context"), ensure_ascii=False),
                    "context_used": normalize_text(response.get("context_used")),
                }
            )

            history.append({"role": "user", "content": step.message})
            history.append({"role": "assistant", "content": normalize_text(response.get("agent_response"))})

            print(f"Paso {step.step_number}: {step.message}")
            print(f"Respuesta: {normalize_text(response.get('agent_response'))}")

            if response.get("order_created") and not order_created_at_step:
                order_created_at_step = step.step_number
                order_rows.append(
                    {
                        "scenario_id": scenario.scenario_id,
                        "vendor_id": vendor_id,
                        "customer_name": scenario.customer_name,
                        "product_name": scenario.product_name,
                        "order_id": response["order_created"].get("id"),
                        "status": response["order_created"].get("status"),
                        "total_amount": response["order_created"].get("total_amount"),
                        "created_at": response["order_created"].get("created_at"),
                        "step_created": step.step_number,
                        "agent_response": normalize_text(response.get("agent_response")),
                    }
                )

        latest_order = find_latest_order(db, vendor_id)
        print(f"Orden creada en DB: {'si' if latest_order else 'no'}")
        if latest_order:
            print(f"Ultima orden: #{latest_order.id} - {latest_order.customer_name} - {latest_order.total_amount}")

    after_count = fetch_current_order_count(db)

    summary_rows = [
        {"metric": "Ordenes antes", "value": before_count},
        {"metric": "Ordenes despues", "value": after_count},
        {"metric": "Nuevas ordenes", "value": after_count - before_count},
        {"metric": "Conversaciones ejecutadas", "value": len(scenarios)},
        {"metric": "Conversaciones con orden", "value": len(order_rows)},
        {"metric": "Tasa de conversacion a orden (%)", "value": round(len(order_rows) / len(scenarios) * 100, 2) if scenarios else 0.0},
    ]

    detail_df = pd.DataFrame(detail_rows)
    orders_df = pd.DataFrame(order_rows)
    summary_df = pd.DataFrame(summary_rows)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_df.to_excel(writer, index=False, sheet_name="resumen")
        orders_df.to_excel(writer, index=False, sheet_name="ordenes_creadas")
        detail_df.to_excel(writer, index=False, sheet_name="detalle_mensajes")

    print("\n=== RESUMEN FINAL ===")
    print(f"Ordenes antes: {before_count}")
    print(f"Ordenes despues: {after_count}")
    print(f"Nuevas ordenes creadas: {after_count - before_count}")
    print(f"Conversaciones que crearon orden: {len(order_rows)} de {len(scenarios)}")
    print(f"Excel generado en: {output_path}")

    return 0 if len(order_rows) == len(scenarios) else 1


if __name__ == "__main__":
    raise SystemExit(main())
