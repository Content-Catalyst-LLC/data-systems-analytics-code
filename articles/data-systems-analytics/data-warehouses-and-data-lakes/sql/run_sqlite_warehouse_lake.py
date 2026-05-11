#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "warehouse_lake.sqlite"

TABLES = {
    "data_assets": ROOT / "data" / "data_assets.csv",
    "dimensional_model_tables": ROOT / "data" / "dimensional_model_tables.csv",
    "lake_zones": ROOT / "data" / "lake_zones.csv",
    "governance_controls": ROOT / "data" / "governance_controls.csv",
    "cost_performance_metrics": ROOT / "data" / "cost_performance_metrics.csv",
    "lakehouse_table_features": ROOT / "data" / "lakehouse_table_features.csv",
    "workload_requirements": ROOT / "data" / "workload_requirements.csv",
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

print(f"SQLite warehouse/lake database written to {DB}")
print("Assets requiring governance review:")
for row in conn.execute("""
    SELECT a.asset_name, a.architecture_zone, g.metadata_coverage, g.lineage_coverage, g.access_policy_status, g.certification_status
    FROM data_assets a
    JOIN governance_controls g ON a.asset_id = g.asset_id
    WHERE g.metadata_coverage < 0.70 OR g.lineage_coverage < 0.60 OR g.access_policy_status IN ('missing', 'unknown')
    ORDER BY g.metadata_coverage, g.lineage_coverage
"""):
    print(row)

conn.close()
