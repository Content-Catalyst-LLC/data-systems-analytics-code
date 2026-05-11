#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "database_architecture.sqlite"

TABLES = {
    "system_inventory": ROOT / "data" / "system_inventory.csv",
    "schema_assets": ROOT / "data" / "schema_assets.csv",
    "workload_catalog": ROOT / "data" / "workload_catalog.csv",
    "governance_controls": ROOT / "data" / "governance_controls.csv",
    "recovery_plans": ROOT / "data" / "recovery_plans.csv",
    "integration_lineage": ROOT / "data" / "integration_lineage.csv",
    "architecture_risks": ROOT / "data" / "architecture_risks.csv",
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

print(f"SQLite database architecture review database written to {DB}")
print("Governance controls requiring review:")
for row in conn.execute("""
    SELECT s.system_name, g.metadata_coverage, g.lineage_coverage, g.access_policy_status, g.recovery_test_status, g.quality_gate_status
    FROM governance_controls g
    JOIN system_inventory s ON s.system_id = g.system_id
    WHERE g.metadata_coverage < 0.85 OR g.lineage_coverage < 0.75 OR g.recovery_test_status <> 'pass' OR g.quality_gate_status <> 'pass'
    ORDER BY g.metadata_coverage, g.lineage_coverage
"""):
    print(row)

conn.close()
