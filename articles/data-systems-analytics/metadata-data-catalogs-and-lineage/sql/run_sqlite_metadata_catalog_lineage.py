#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "metadata_catalog_lineage.sqlite"

TABLES = {
    "data_assets": ROOT / "data" / "data_assets.csv",
    "metadata_elements": ROOT / "data" / "metadata_elements.csv",
    "catalog_entries": ROOT / "data" / "catalog_entries.csv",
    "glossary_terms": ROOT / "data" / "glossary_terms.csv",
    "lineage_edges": ROOT / "data" / "lineage_edges.csv",
    "provenance_events": ROOT / "data" / "provenance_events.csv",
    "policy_tags": ROOT / "data" / "policy_tags.csv",
    "quality_signals": ROOT / "data" / "quality_signals.csv",
    "catalog_usage": ROOT / "data" / "catalog_usage.csv",
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

print(f"SQLite metadata/catalog/lineage database written to {DB}")
print("Catalog trust labels:")
for row in conn.execute("""
    SELECT trust_label, COUNT(*)
    FROM catalog_entries
    GROUP BY trust_label
    ORDER BY trust_label
"""):
    print(row)

conn.close()
