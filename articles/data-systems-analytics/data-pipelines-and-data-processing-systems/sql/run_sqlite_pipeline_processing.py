#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "pipeline_processing.sqlite"

TABLES = {
    "pipeline_stages": ROOT / "data" / "pipeline_stages.csv",
    "pipeline_runs": ROOT / "data" / "pipeline_runs.csv",
    "quality_gates": ROOT / "data" / "quality_gates.csv",
    "observability_metrics": ROOT / "data" / "observability_metrics.csv",
    "lineage_edges": ROOT / "data" / "lineage_edges.csv",
    "backfill_requests": ROOT / "data" / "backfill_requests.csv",
    "idempotency_checks": ROOT / "data" / "idempotency_checks.csv",
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

print(f"SQLite pipeline processing database written to {DB}")
print("Quality gates requiring review:")
for row in conn.execute("""
    SELECT pipeline_name, stage_name, rule_name, observed_value, threshold, severity, status
    FROM quality_gates
    WHERE status <> 'pass' OR observed_value < threshold
    ORDER BY severity DESC, pipeline_name, stage_name
"""):
    print(row)

conn.close()
