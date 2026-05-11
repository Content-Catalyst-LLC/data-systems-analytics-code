#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "cloud_data_platform.sqlite"

TABLES = {
    "stack_components": ROOT / "data" / "stack_components.csv",
    "pipeline_catalog": ROOT / "data" / "pipeline_catalog.csv",
    "access_policies": ROOT / "data" / "access_policies.csv",
    "cost_events": ROOT / "data" / "cost_events.csv",
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

print(f"SQLite architecture database written to {DB}")
print("Layer coverage:")
for row in conn.execute("SELECT layer, COUNT(*) FROM stack_components GROUP BY layer ORDER BY layer"):
    print(row)

conn.close()
