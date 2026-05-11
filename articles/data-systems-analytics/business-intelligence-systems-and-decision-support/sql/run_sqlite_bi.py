#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "business_intelligence_decision_support.sqlite"

TABLES = {
    "bi_metrics": ROOT / "data" / "bi_metrics.csv",
    "dashboard_inventory": ROOT / "data" / "dashboard_inventory.csv",
    "decision_thresholds": ROOT / "data" / "decision_thresholds.csv",
    "alert_events": ROOT / "data" / "alert_events.csv",
    "decision_reviews": ROOT / "data" / "decision_reviews.csv",
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

print(f"SQLite BI database written to {DB}")
print("Certified dashboard coverage:")
for row in conn.execute("""
    SELECT domain, COUNT(*) AS dashboard_count,
           SUM(CASE WHEN certification_status = 'certified' THEN 1 ELSE 0 END) AS certified_dashboards
    FROM dashboard_inventory
    GROUP BY domain
    ORDER BY domain
"""):
    print(row)

conn.close()
