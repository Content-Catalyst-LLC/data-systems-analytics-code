#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "data_visualization_integrity.sqlite"

TABLES = {
    "visualization_inventory": ROOT / "data" / "visualization_inventory.csv",
    "chart_assessments": ROOT / "data" / "chart_assessments.csv",
    "encoding_assessments": ROOT / "data" / "encoding_assessments.csv",
    "uncertainty_elements": ROOT / "data" / "uncertainty_elements.csv",
    "annotation_elements": ROOT / "data" / "annotation_elements.csv",
    "accessibility_checks": ROOT / "data" / "accessibility_checks.csv",
    "evidence_links": ROOT / "data" / "evidence_links.csv",
    "audience_contexts": ROOT / "data" / "audience_contexts.csv",
    "review_checkpoints": ROOT / "data" / "review_checkpoints.csv",
    "visual_outputs": ROOT / "data" / "visual_outputs.csv",
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

print(f"SQLite visualization-integrity database written to {DB}")
print("Visualization issues requiring review:")
for row in conn.execute("""
    SELECT visual_id, visual_title, status, publication_surface
    FROM visualization_inventory
    WHERE status <> 'approved'
    ORDER BY status, visual_id
"""):
    print(row)

conn.close()
