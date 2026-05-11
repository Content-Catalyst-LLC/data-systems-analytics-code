#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "streaming_analytics.sqlite"

TABLES = {
    "event_stream": ROOT / "data" / "event_stream.csv",
    "stream_topic_registry": ROOT / "data" / "stream_topic_registry.csv",
    "window_definitions": ROOT / "data" / "window_definitions.csv",
    "watermark_observations": ROOT / "data" / "watermark_observations.csv",
    "alert_rules": ROOT / "data" / "alert_rules.csv",
    "governance_checks": ROOT / "data" / "governance_checks.csv",
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

print(f"SQLite streaming analytics database written to {DB}")
print("Governance checks requiring review:")
for row in conn.execute("""
    SELECT check_type, status, severity, remediation
    FROM governance_checks
    WHERE status <> 'pass'
    ORDER BY severity DESC, check_type
"""):
    print(row)

conn.close()
