#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_governance_stewardship.sqlite"

TABLES = {
    "data_assets": ROOT / "data" / "data_assets.csv",
    "stewardship_roles": ROOT / "data" / "stewardship_roles.csv",
    "decision_rights": ROOT / "data" / "decision_rights.csv",
    "policy_register": ROOT / "data" / "policy_register.csv",
    "quality_issues": ROOT / "data" / "quality_issues.csv",
    "access_reviews": ROOT / "data" / "access_reviews.csv",
    "lifecycle_controls": ROOT / "data" / "lifecycle_controls.csv",
    "responsible_use_risks": ROOT / "data" / "responsible_use_risks.csv",
    "governance_events": ROOT / "data" / "governance_events.csv",
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

print(f"SQLite governance database written to {DB}")
print("Open or in-review quality issues:")
for row in conn.execute("""
    SELECT asset_id, issue_type, severity, status, assigned_steward
    FROM quality_issues
    WHERE status <> 'resolved'
    ORDER BY severity DESC
"""):
    print(row)

conn.close()
