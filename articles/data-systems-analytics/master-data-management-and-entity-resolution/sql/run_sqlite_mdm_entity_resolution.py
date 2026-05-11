#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "mdm_entity_resolution.sqlite"

TABLES = {
    "source_records": ROOT / "data" / "source_records.csv",
    "candidate_matches": ROOT / "data" / "candidate_matches.csv",
    "master_entities": ROOT / "data" / "master_entities.csv",
    "entity_crosswalk": ROOT / "data" / "entity_crosswalk.csv",
    "survivorship_rules": ROOT / "data" / "survivorship_rules.csv",
    "hierarchy_edges": ROOT / "data" / "hierarchy_edges.csv",
    "stewardship_queue": ROOT / "data" / "stewardship_queue.csv",
    "external_identifiers": ROOT / "data" / "external_identifiers.csv",
    "privacy_identity_risk": ROOT / "data" / "privacy_identity_risk.csv",
    "mdm_lineage_events": ROOT / "data" / "mdm_lineage_events.csv",
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

print(f"SQLite MDM/entity-resolution database written to {DB}")
print("Candidate matches requiring review:")
for row in conn.execute("""
    SELECT candidate_id, entity_type, match_score, recommended_action
    FROM candidate_matches
    WHERE review_required = 'true'
    ORDER BY match_score DESC
"""):
    print(row)

conn.close()
