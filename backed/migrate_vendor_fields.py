#!/usr/bin/env python
"""Add missing vendor fields to the database."""

import os
from sqlalchemy import text, inspect
from app.infrastructure.db.session import engine, SessionLocal

def add_missing_columns():
    """Add missing columns to vendors table if they don't exist."""
    
    # Columns to add with proper defaults
    columns_to_add = {
        'rfc': ('VARCHAR(50)', None),
        'sector': ('VARCHAR(100)', None),
        'phone': ('VARCHAR(50)', None),
        'website': ('VARCHAR(255)', None),
        'address': ('VARCHAR(500)', None),
        'city': ('VARCHAR(100)', None),
        'state': ('VARCHAR(100)', None),
        'country': ('VARCHAR(100)', 'México'),
        'postal_code': ('VARCHAR(20)', None),
        'description': ('TEXT', None),
    }
    
    inspector = inspect(engine)
    existing_columns = {col['name'] for col in inspector.get_columns('vendors')}
    
    print("📋 Current columns in vendors table:")
    for col in existing_columns:
        print(f"  ✓ {col}")
    
    print("\n🔍 Checking for missing columns...")
    
    missing_columns = {}
    for col_name, (col_type, default_val) in columns_to_add.items():
        if col_name not in existing_columns:
            missing_columns[col_name] = (col_type, default_val)
            print(f"  ✗ Missing: {col_name}")
        else:
            print(f"  ✓ Already exists: {col_name}")
    
    if not missing_columns:
        print("\n✅ All columns already exist! No migration needed.")
        return
    
    print(f"\n🔧 Adding {len(missing_columns)} missing columns...")
    
    for col_name, (col_type, default_val) in missing_columns.items():
        connection = engine.connect()
        try:
            if default_val is not None:
                sql = f"ALTER TABLE vendors ADD COLUMN {col_name} {col_type} DEFAULT '{default_val}'"
            else:
                sql = f"ALTER TABLE vendors ADD COLUMN {col_name} {col_type}"
            connection.execute(text(sql))
            connection.commit()
            print(f"  ✅ Added: {col_name}")
        except Exception as e:
            connection.rollback()
            print(f"  ⚠️  Error adding {col_name}: {str(e)}")
        finally:
            connection.close()
    
    print("\n✅ Migration completed successfully!")

if __name__ == "__main__":
    try:
        print("🚀 Starting database migration...\n")
        add_missing_columns()
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        exit(1)
