#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_products_self_service.sqlite"

TABLES = {
    "data_products": ROOT / "data" / "data_products.csv",
    "semantic_metrics": ROOT / "data" / "semantic_metrics.csv",
    "access_events": ROOT / "data" / "access_events.csv",
    "quality_checks": ROOT / "data" / "quality_checks.csv",
    "product_lineage": ROOT / "data" / "product_lineage.csv",
}

DB.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))

for table, path in TABLES.items():
    conn.execute(f"DELETE FROM {table}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        placeholders = ",".join([f":{col}" for col in columns])
        column_sql = ",".join(columns)
        conn.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            reader,
        )

conn.commit()

print(f"SQLite product database written to {DB}")
print("Products by domain:")
for row in conn.execute("""
    SELECT domain, COUNT(*) AS product_count, ROUND(AVG(quality_score), 3)
    FROM data_products
    GROUP BY domain
    ORDER BY domain
"""):
    print(row)

conn.close()
