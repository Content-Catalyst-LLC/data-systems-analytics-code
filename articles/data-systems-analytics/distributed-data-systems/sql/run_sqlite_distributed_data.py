#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "distributed_data.sqlite"

TABLES = {
    "cluster_nodes": ROOT / "data" / "cluster_nodes.csv",
    "shard_map": ROOT / "data" / "shard_map.csv",
    "replica_status": ROOT / "data" / "replica_status.csv",
    "quorum_policies": ROOT / "data" / "quorum_policies.csv",
    "operation_log": ROOT / "data" / "operation_log.csv",
    "conflict_records": ROOT / "data" / "conflict_records.csv",
    "consensus_events": ROOT / "data" / "consensus_events.csv",
    "failover_drills": ROOT / "data" / "failover_drills.csv",
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

print(f"SQLite distributed data database written to {DB}")
print("Replicas requiring review:")
for row in conn.execute("""
    SELECT shard_id, node_id, lag_ops, replica_state
    FROM replica_status
    WHERE replica_state <> 'in_sync' OR lag_ops > 50
    ORDER BY lag_ops DESC
"""):
    print(row)

conn.close()
