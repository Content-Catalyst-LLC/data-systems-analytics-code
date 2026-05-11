#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "etl_transformation.sqlite"

TABLES = {
    "raw_customer_extract": ROOT / "data" / "raw_customer_extract.csv",
    "raw_order_extract": ROOT / "data" / "raw_order_extract.csv",
    "status_mapping": ROOT / "data" / "status_mapping.csv",
    "cdc_events": ROOT / "data" / "cdc_events.csv",
    "transformation_tests": ROOT / "data" / "transformation_tests.csv",
    "orchestration_runs": ROOT / "data" / "orchestration_runs.csv",
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
        rows = []
        for row in reader:
            if table == "raw_customer_extract" and row.get("email") == "":
                row["email"] = None
            if table == "cdc_events" and row.get("payload_amount") == "":
                row["payload_amount"] = None
            rows.append(row)
        conn.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            rows,
        )

conn.commit()

print(f"SQLite ETL transformation database written to {DB}")
print("Transformation tests requiring review:")
for row in conn.execute("""
    SELECT scope, test_name, status, severity
    FROM transformation_tests
    WHERE status <> 'pass'
    ORDER BY severity DESC, scope, test_name
"""):
    print(row)

conn.close()
