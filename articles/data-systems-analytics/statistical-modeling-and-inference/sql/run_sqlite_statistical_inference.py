#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "statistical_inference.sqlite"

TABLES = {
    "sample_observations": ROOT / "data" / "sample_observations.csv",
    "model_registry": ROOT / "data" / "model_registry.csv",
    "inference_claims": ROOT / "data" / "inference_claims.csv",
    "diagnostic_checks": ROOT / "data" / "diagnostic_checks.csv",
    "robustness_checks": ROOT / "data" / "robustness_checks.csv",
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

print(f"SQLite statistical inference database written to {DB}")
print("Diagnostics requiring review:")
for row in conn.execute("""
    SELECT model_id, check_type, status, severity, remediation
    FROM diagnostic_checks
    WHERE status <> 'pass'
    ORDER BY severity DESC, model_id
"""):
    print(row)

conn.close()
