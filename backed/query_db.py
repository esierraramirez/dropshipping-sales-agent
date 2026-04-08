import sqlite3

conn = sqlite3.connect('catalog.db')
c = conn.cursor()

print("===== VENDORS =====")
for row in c.execute("SELECT id, name, slug FROM vendors"):
    print(f"  {row[0]}: {row[1]} (slug: {row[2]})")

print("\n===== PRODUCTOS POR VENDOR =====")
for vendor_id, vendor_name in c.execute("SELECT id, name FROM vendors"):
    count = len(list(c.execute("SELECT id FROM products WHERE vendor_id = ?", (vendor_id,))))
    print(f"{vendor_name}: {count} productos")

conn.close()
print("\n✓ Consulta completada")
