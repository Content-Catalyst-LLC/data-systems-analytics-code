#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "feature_engineering.sqlite"

TABLES = {
    "feature_registry": ROOT / "data" / "feature_registry.csv",
    "transformation_rules": ROOT / "data" / "transformation_rules.csv",
    "feature_quality_checks": ROOT / "data" / "feature_quality_checks.csv",
    "selection_scores": ROOT / "data" / "selection_scores.csv",
    "representation_metrics": ROOT / "data" / "representation_metrics.csv",
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

print(f"SQLite feature-engineering database written to {DB}")
print("Features requiring leakage or review attention:")
for row in conn.execute("""
    SELECT feature_name, feature_family, leakage_risk, status
    FROM feature_registry
    WHERE leakage_risk <> 'low' OR status <> 'approved'
    ORDER BY leakage_risk DESC, feature_name
"""):
    print(row)

conn.close()
