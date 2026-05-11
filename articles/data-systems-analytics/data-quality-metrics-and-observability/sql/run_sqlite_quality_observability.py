#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_quality_observability.sqlite"

TABLES = {
    "dataset_registry": ROOT / "data" / "dataset_registry.csv",
    "quality_checks": ROOT / "data" / "quality_checks.csv",
    "observability_events": ROOT / "data" / "observability_events.csv",
    "baselines": ROOT / "data" / "baselines.csv",
    "incidents": ROOT / "data" / "incidents.csv",
    "lineage_impact": ROOT / "data" / "lineage_impact.csv",
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

print(f"SQLite quality observability database written to {DB}")
print("Quality check status by dimension:")
for row in conn.execute("""
    SELECT quality_dimension, status, COUNT(*)
    FROM quality_checks
    GROUP BY quality_dimension, status
    ORDER BY quality_dimension, status
"""):
    print(row)

conn.close()
