#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "causal_inference.sqlite"

TABLES = {
    "causal_study_registry": ROOT / "data" / "causal_study_registry.csv",
    "experiment_units": ROOT / "data" / "experiment_units.csv",
    "did_panel": ROOT / "data" / "did_panel.csv",
    "rdd_units": ROOT / "data" / "rdd_units.csv",
    "assumption_checks": ROOT / "data" / "assumption_checks.csv",
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

print(f"SQLite causal inference database written to {DB}")
print("Assumption checks requiring review:")
for row in conn.execute("""
    SELECT study_id, assumption, status, severity, remediation
    FROM assumption_checks
    WHERE status <> 'pass'
    ORDER BY severity DESC, study_id
"""):
    print(row)

conn.close()
