#!/usr/bin/env python3
"""
SQLite loader for the article's SQL examples.
Uses Python's standard sqlite3 module so the SQL can be tested locally.
"""

import csv
import sqlite3
from pathlib import Path

root = Path.cwd()
db_path = root / "outputs" / "reproducible_analytics.sqlite"
db_path.parent.mkdir(parents=True, exist_ok=True)

schema = (root / "sql" / "schema.sql").read_text(encoding="utf-8")
queries = (root / "sql" / "reproducibility_queries.sql").read_text(encoding="utf-8")

conn = sqlite3.connect(db_path)
conn.executescript(schema)
conn.execute("DELETE FROM analytics_events")

with (root / "data" / "sample_events.csv").open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    conn.executemany(
        """
        INSERT INTO analytics_events (event_date, region, system, event_type, value)
        VALUES (:event_date, :region, :system, :event_type, :value)
        """,
        reader,
    )

conn.commit()

print(f"SQLite database written to {db_path}")
print("Summary query result:")
for row in conn.execute("""
    SELECT system, COUNT(*) AS records, SUM(value) AS total_value, ROUND(AVG(value), 2) AS average_value
    FROM analytics_events
    GROUP BY system
    ORDER BY system
"""):
    print(row)

conn.close()
