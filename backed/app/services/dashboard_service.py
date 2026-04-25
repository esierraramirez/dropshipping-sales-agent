from pathlib import Path
from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.models.product import Product
from app.models.order import Order
from app.models.whatsapp_connection import WhatsAppConnection


def build_dashboard_data(db: Session, vendor: Vendor) -> dict:
    settings = (
        db.query(VendorSettings)
        .filter(VendorSettings.vendor_id == vendor.id)
        .first()
    )

    total_products = (
        db.query(Product)
        .filter(
            Product.vendor_id == vendor.id,
            Product.is_deleted == False
        )
        .count()
    )

    vendor_slug = vendor.slug
    kb_path = Path("data/index") / vendor_slug / "knowledge_base.jsonl"
    knowledge_base_ready = kb_path.exists()

    orders = (
        db.query(Order)
        .filter(Order.vendor_id == vendor.id)
        .all()
    )

    in_process_orders = len([o for o in orders if o.status == "en_proceso"])
    shipped_orders = len([o for o in orders if o.status == "enviado"])
    delivered_orders = len([o for o in orders if o.status == "entregado"])
    cancelled_orders = len([o for o in orders if o.status == "cancelado"])

    whatsapp = (
        db.query(WhatsAppConnection)
        .filter(WhatsAppConnection.vendor_id == vendor.id)
        .first()
    )

    return {
        "vendor": {
            "id": vendor.id,
            "name": vendor.name,
            "slug": vendor.slug,
            "email": vendor.email,
            "is_active": vendor.is_active,
        },
        "settings": {
            "business_start_hour": settings.business_start_hour if settings else None,
            "business_end_hour": settings.business_end_hour if settings else None,
            "off_hours_message": settings.off_hours_message if settings else None,
            "agent_enabled": settings.agent_enabled if settings else True,
            "tone": settings.tone if settings else None,
        },
        "catalog": {
            "total_products": total_products,
            "knowledge_base_ready": knowledge_base_ready,
        },
        "orders": {
            "total_orders": len(orders),
            "pending_orders": in_process_orders,
            "confirmed_orders": 0,
            "processed_orders": in_process_orders,
            "shipped_orders": shipped_orders,
            "delivered_orders": delivered_orders,
            "cancelled_orders": cancelled_orders,
        },
        "whatsapp": {
            "is_connected": whatsapp.is_connected if whatsapp else False,
            "phone_number_id": whatsapp.phone_number_id if whatsapp else None,
            "business_account_id": whatsapp.business_account_id if whatsapp else None,
        }
    }
