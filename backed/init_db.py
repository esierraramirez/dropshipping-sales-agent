#!/usr/bin/env python
"""Initialize the database with all tables."""

from app.infrastructure.db.session import Base, engine
from app.models.vendor import Vendor
from app.models.product import Product

if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("Tables created:")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")
