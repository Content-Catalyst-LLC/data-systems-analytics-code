#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "analytics_engineering_semantic_layer.sqlite"

TABLES = {
    "model_registry": ROOT / "data" / "model_registry.csv",
    "semantic_metrics": ROOT / "data" / "semantic_metrics.csv",
    "model_tests": ROOT / "data" / "model_tests.csv",
    "semantic_lineage": ROOT / "data" / "semantic_lineage.csv",
    "metric_usage": ROOT / "data" / "metric_usage.csv",
    "definition_drift": ROOT / "data" / "definition_drift.csv",
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

print(f"SQLite semantic layer database written to {DB}")
print("Metric certification by domain:")
for row in conn.execute("""
    SELECT domain, certification_status, COUNT(*)
    FROM semantic_metrics
    GROUP BY domain, certification_status
    ORDER BY domain, certification_status
"""):
    print(row)

conn.close()
