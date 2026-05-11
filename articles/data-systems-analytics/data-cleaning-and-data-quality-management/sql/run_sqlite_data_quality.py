#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_quality.sqlite"

TABLES = {
    "raw_customer_records": ROOT / "data" / "raw_customer_records.csv",
    "quality_rules": ROOT / "data" / "quality_rules.csv",
    "status_mapping": ROOT / "data" / "status_mapping.csv",
    "root_cause_register": ROOT / "data" / "root_cause_register.csv",
    "quality_incidents": ROOT / "data" / "quality_incidents.csv",
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
            if table == "raw_customer_records" and row.get("email") == "":
                row["email"] = None
            rows.append(row)
        conn.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            rows,
        )

conn.commit()

print(f"SQLite data quality database written to {DB}")
print("Open quality incidents:")
for row in conn.execute("""
    SELECT incident_id, rule_id, failed_records, affected_metric, incident_status
    FROM quality_incidents
    WHERE incident_status <> 'closed'
    ORDER BY detected_at
"""):
    print(row)

conn.close()
