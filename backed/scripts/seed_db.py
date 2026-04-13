from app.infrastructure.db.session import SessionLocal
from app.models.order import Order
from app.models.product import Product
from app.models.vendor import Vendor
from app.models.vendor_settings import VendorSettings
from app.models.whatsapp_connection import WhatsAppConnection


def run_seed() -> None:
    db = SessionLocal()
    try:
        vendor = db.query(Vendor).filter(Vendor.slug == "tienda-demo").first()
        if vendor:
            print("Seed ya existia")
            return

        vendor = Vendor(
            name="Tienda Demo",
            slug="tienda-demo",
            email="demo@tienda.com",
            password_hash="demo-hash",
            is_active=True,
        )
        db.add(vendor)
        db.flush()

        db.add(
            VendorSettings(
                vendor_id=vendor.id,
                business_start_hour="09:00",
                business_end_hour="18:00",
                agent_enabled=True,
                tone="profesional",
            )
        )

        db.add(
            Product(
                vendor_id=vendor.id,
                product_id="P-001",
                name="Producto Demo",
                category="General",
                price=99.99,
                currency="COP",
                stock_status="in_stock",
                min_shipping_days=2,
                max_shipping_days=5,
                short_description="Producto de prueba",
                full_description="Producto demo para validar base de datos",
                brand="DemoBrand",
                shipping_cost=0.0,
                shipping_regions="CO",
                returns_policy="7 dias",
                warranty_policy="30 dias",
                specs="{}",
                variants="[]",
                source="seed",
            )
        )

        db.add(
            Order(
                vendor_id=vendor.id,
                customer_name="Cliente Demo",
                customer_phone="3000000000",
                customer_address="Calle Demo 123",
                items_json='[{"product_id":"P-001","qty":1}]',
                total_amount=99.99,
                status="pending",
            )
        )

        db.add(
            WhatsAppConnection(
                vendor_id=vendor.id,
                phone_number_id="123456789",
                business_account_id="biz_demo",
                access_token="token_demo",
                verify_token="verify_demo",
                is_connected=False,
            )
        )

        db.commit()
        print("Seed creado OK")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
