#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "security_privacy_access.sqlite"

TABLES = {
    "data_assets": ROOT / "data" / "data_assets.csv",
    "access_policies": ROOT / "data" / "access_policies.csv",
    "entitlements": ROOT / "data" / "entitlements.csv",
    "privacy_purposes": ROOT / "data" / "privacy_purposes.csv",
    "audit_events": ROOT / "data" / "audit_events.csv",
    "data_flows": ROOT / "data" / "data_flows.csv",
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

print(f"SQLite security/privacy database written to {DB}")
print("Assets by classification:")
for row in conn.execute("""
    SELECT classification, COUNT(*), ROUND(AVG(sensitivity_score), 3)
    FROM data_assets
    GROUP BY classification
    ORDER BY AVG(sensitivity_score) DESC
"""):
    print(row)

conn.close()
