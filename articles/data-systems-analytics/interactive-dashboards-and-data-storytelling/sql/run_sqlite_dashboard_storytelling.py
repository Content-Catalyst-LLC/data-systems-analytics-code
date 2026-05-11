#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "interactive_dashboards_storytelling.sqlite"

TABLES = {
    "dashboard_inventory": ROOT / "data" / "dashboard_inventory.csv",
    "kpi_definitions": ROOT / "data" / "kpi_definitions.csv",
    "filter_controls": ROOT / "data" / "filter_controls.csv",
    "linked_views": ROOT / "data" / "linked_views.csv",
    "story_points": ROOT / "data" / "story_points.csv",
    "annotations": ROOT / "data" / "annotations.csv",
    "interaction_events": ROOT / "data" / "interaction_events.csv",
    "accessibility_checks": ROOT / "data" / "accessibility_checks.csv",
    "governance_checks": ROOT / "data" / "governance_checks.csv",
    "evidence_links": ROOT / "data" / "evidence_links.csv",
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

print(f"SQLite dashboard/storytelling database written to {DB}")
print("Dashboard clutter-risk candidates:")
for row in conn.execute("""
    SELECT dashboard_id, dashboard_type, view_count, filter_count, status
    FROM dashboard_inventory
    WHERE view_count > 3 OR filter_count > 5
    ORDER BY view_count DESC, filter_count DESC
"""):
    print(row)

conn.close()
