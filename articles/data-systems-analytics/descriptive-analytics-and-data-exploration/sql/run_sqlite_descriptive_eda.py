#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "descriptive_eda.sqlite"

TABLES = {
    "exploration_dataset": ROOT / "data" / "exploration_dataset.csv",
    "variable_profile": ROOT / "data" / "variable_profile.csv",
    "exploration_checks": ROOT / "data" / "exploration_checks.csv",
    "exploration_questions": ROOT / "data" / "exploration_questions.csv",
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

        rows = []
        for row in reader:
            if table == "exploration_dataset" and row.get("value") == "NA":
                row["value"] = None
            rows.append(row)

        conn.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            rows,
        )

conn.commit()

print(f"SQLite descriptive EDA database written to {DB}")
print("Exploration checks requiring review:")
for row in conn.execute("""
    SELECT check_type, status, severity, remediation
    FROM exploration_checks
    WHERE status <> 'pass'
    ORDER BY severity DESC, check_type
"""):
    print(row)

conn.close()
