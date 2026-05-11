#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_integration_interoperability.sqlite"

TABLES = {
    "source_systems": ROOT / "data" / "source_systems.csv",
    "schema_mappings": ROOT / "data" / "schema_mappings.csv",
    "entity_crosswalk": ROOT / "data" / "entity_crosswalk.csv",
    "interoperability_checks": ROOT / "data" / "interoperability_checks.csv",
    "lineage_events": ROOT / "data" / "lineage_events.csv",
    "message_payloads": ROOT / "data" / "message_payloads.csv",
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

print(f"SQLite interoperability database written to {DB}")
print("Interoperability checks by layer:")
for row in conn.execute("""
    SELECT layer, status, COUNT(*)
    FROM interoperability_checks
    GROUP BY layer, status
    ORDER BY layer, status
"""):
    print(row)

conn.close()
