#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "model_evaluation.sqlite"

TABLES = {
    "model_registry": ROOT / "data" / "model_registry.csv",
    "binary_predictions": ROOT / "data" / "binary_predictions.csv",
    "regression_predictions": ROOT / "data" / "regression_predictions.csv",
    "threshold_policies": ROOT / "data" / "threshold_policies.csv",
    "metric_scorecard": ROOT / "data" / "metric_scorecard.csv",
    "monitoring_windows": ROOT / "data" / "monitoring_windows.csv",
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

print(f"SQLite model-evaluation database written to {DB}")
print("Monitoring windows requiring review:")
for row in conn.execute("""
    SELECT model_id, window_start, window_end, drift_index, status
    FROM monitoring_windows
    WHERE status <> 'approved' OR drift_index >= 0.18
    ORDER BY model_id, window_start
"""):
    print(row)

conn.close()
