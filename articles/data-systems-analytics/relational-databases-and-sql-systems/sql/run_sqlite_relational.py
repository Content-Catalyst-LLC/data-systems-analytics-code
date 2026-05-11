#!/usr/bin/env python3
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "relational_sql.sqlite"
DB.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON;")
conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
conn.executescript((ROOT / "sql" / "sample_data.sql").read_text(encoding="utf-8"))

print(f"SQLite relational database written to {DB}")
print("Daily revenue report:")
for row in conn.execute("""
    SELECT o.order_date, p.payment_status, SUM(p.amount) AS total_payment_amount, COUNT(DISTINCT o.order_id) AS order_count
    FROM orders o
    JOIN payments p ON p.order_id = o.order_id
    GROUP BY o.order_date, p.payment_status
    ORDER BY o.order_date
"""):
    print(row)

print("Foreign key enforcement test:")
try:
    conn.execute("INSERT INTO orders(order_id, customer_id, order_date, status) VALUES (9999, 999, '2026-05-11', 'created')")
    conn.commit()
except sqlite3.IntegrityError as exc:
    print(f"expected_integrity_error={exc}")

conn.close()
