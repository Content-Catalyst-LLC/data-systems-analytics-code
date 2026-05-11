#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "predictive_analytics.sqlite"

TABLES = {
    "model_registry": ROOT / "data" / "model_registry.csv",
    "classification_predictions": ROOT / "data" / "classification_predictions.csv",
    "regression_predictions": ROOT / "data" / "regression_predictions.csv",
    "training_validation_splits": ROOT / "data" / "training_validation_splits.csv",
    "threshold_policies": ROOT / "data" / "threshold_policies.csv",
    "metric_scorecard": ROOT / "data" / "metric_scorecard.csv",
    "leakage_shift_checks": ROOT / "data" / "leakage_shift_checks.csv",
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

print(f"SQLite predictive-analytics database written to {DB}")
print("Models requiring governance attention:")
for row in conn.execute("""
    SELECT model_id, model_name, task_type, status, risk_level
    FROM model_registry
    WHERE status <> 'approved'
    ORDER BY risk_level DESC, status, model_id
"""):
    print(row)

conn.close()
