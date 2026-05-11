#!/usr/bin/env python3
"""
Python Workflow: Distributed Data Systems Quorum, Replication, and Readiness Scorecard

This workflow evaluates shard placement, quorum policy, replica lag, operations,
conflicts, consensus events, failover drills, and distributed-system readiness
using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import statistics
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

def stable_hash(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "healthy": 1.0,
        "success": 1.0,
        "resolved": 0.9,
        "in_review": 0.65,
        "warn": 0.45,
        "pending": 0.35,
        "lagging": 0.45,
        "degraded": 0.25,
        "partial": 0.25,
        "failed": 0.0,
    }.get(value, 0.5)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def quorum_intersection(replication_factor: int, read_quorum: int, write_quorum: int) -> int:
    return int(read_quorum + write_quorum > replication_factor)

def tolerate_failures(replication_factor: int) -> int:
    return max(0, (replication_factor - 1) // 2)

def key_to_shard(key: str, shard_map: list[dict[str, str]]) -> str:
    bucket = stable_hash(key) % 10000
    for shard in shard_map:
        start = int(shard["key_range_start"])
        end = int(shard["key_range_end"])
        if start <= bucket <= end:
            return shard["shard_id"]
    return "unmapped"

def main() -> None:
    nodes_path = ROOT / "data" / "cluster_nodes.csv"
    shards_path = ROOT / "data" / "shard_map.csv"
    replicas_path = ROOT / "data" / "replica_status.csv"
    policies_path = ROOT / "data" / "quorum_policies.csv"
    operations_path = ROOT / "data" / "operation_log.csv"
    conflicts_path = ROOT / "data" / "conflict_records.csv"
    consensus_path = ROOT / "data" / "consensus_events.csv"
    failover_path = ROOT / "data" / "failover_drills.csv"

    nodes = read_csv(nodes_path)
    shards = read_csv(shards_path)
    replicas = read_csv(replicas_path)
    policies = read_csv(policies_path)
    operations = read_csv(operations_path)
    conflicts = read_csv(conflicts_path)
    consensus = read_csv(consensus_path)
    failovers = read_csv(failover_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()

    # Shard routing examples.
    example_keys = ["user:1001", "order:2050", "cart:9188", "session:8801", "ledger:4555", "profile:3300"]
    routing_rows = []
    for key in example_keys:
        shard_id = key_to_shard(key, shards)
        shard = next((s for s in shards if s["shard_id"] == shard_id), {})
        routing_rows.append({
            "key_id": key,
            "hash_bucket": stable_hash(key) % 10000,
            "assigned_shard": shard_id,
            "leader_node": shard.get("leader_node", ""),
            "replica_nodes": shard.get("replica_nodes", ""),
            "partition_strategy": shard.get("partition_strategy", ""),
        })

    # Quorum policy scorecard.
    quorum_rows = []
    for policy in policies:
        n = int(policy["replication_factor"])
        r = int(policy["read_quorum"])
        w = int(policy["write_quorum"])
        intersects = quorum_intersection(n, r, w)
        write_majority = int(w > n / 2)
        read_majority = int(r > n / 2)
        availability_pressure = (r + w) / (2 * n)
        quorum_rows.append({
            "policy_id": policy["policy_id"],
            "workload": policy["workload"],
            "replication_factor": n,
            "read_quorum": r,
            "write_quorum": w,
            "consistency_model": policy["consistency_model"],
            "availability_orientation": policy["availability_orientation"],
            "read_write_quorums_intersect": intersects,
            "write_majority": write_majority,
            "read_majority": read_majority,
            "tolerated_failures_for_majority": tolerate_failures(n),
            "availability_pressure": round(availability_pressure, 3),
            "policy_score": round(
                0.35 * intersects
                + 0.25 * write_majority
                + 0.20 * status_score(policy["status"])
                + 0.20 * (1.0 - min(availability_pressure, 1.0)),
                3,
            ),
            "status": policy["status"],
        })

    # Replica lag and shard health.
    replicas_by_shard = defaultdict(list)
    for replica in replicas:
        replicas_by_shard[replica["shard_id"]].append(replica)

    shard_rows = []
    for shard in shards:
        shard_replicas = replicas_by_shard[shard["shard_id"]]
        lag_values = [int(r["lag_ops"]) for r in shard_replicas]
        degraded_count = sum(1 for r in shard_replicas if r["replica_state"] != "in_sync")
        leader_present = any(r["is_leader"] == "1" for r in shard_replicas)
        healthy_ratio = sum(1 for r in shard_replicas if r["replica_state"] == "in_sync") / max(len(shard_replicas), 1)
        max_lag = max(lag_values) if lag_values else 0
        lag_score = max(0.0, 1.0 - min(max_lag / 200.0, 1.0))
        health_score = round(0.35 * healthy_ratio + 0.25 * lag_score + 0.20 * int(leader_present) + 0.20 * status_score(shard["status"]), 3)
        shard_rows.append({
            "shard_id": shard["shard_id"],
            "leader_node": shard["leader_node"],
            "replication_factor": shard["replication_factor"],
            "replica_count": len(shard_replicas),
            "max_lag_ops": max_lag,
            "mean_lag_ops": round(mean(lag_values), 3),
            "degraded_replica_count": degraded_count,
            "leader_present": int(leader_present),
            "shard_status": shard["status"],
            "shard_health_score": health_score,
        })

    # Operation health.
    operation_rows = []
    for op in operations:
        latency = float(op["latency_ms"])
        quorum_ok = int(op["result_status"] in {"committed", "served"} and op["consistency_observed"] != "quorum_not_met")
        latency_score = max(0.0, 1.0 - min(latency / 250.0, 1.0))
        operation_rows.append({
            "operation_id": op["operation_id"],
            "shard_id": op["shard_id"],
            "operation_type": op["operation_type"],
            "client_region": op["client_region"],
            "latency_ms": latency,
            "read_quorum_observed": op["read_quorum_observed"],
            "write_quorum_observed": op["write_quorum_observed"],
            "result_status": op["result_status"],
            "consistency_observed": op["consistency_observed"],
            "quorum_ok": quorum_ok,
            "operation_score": round(0.55 * quorum_ok + 0.30 * latency_score + 0.15 * status_score(op["result_status"]), 3),
        })

    conflict_rows = []
    for conflict in conflicts:
        conflict_rows.append({
            "conflict_id": conflict["conflict_id"],
            "shard_id": conflict["shard_id"],
            "key_id": conflict["key_id"],
            "resolution_strategy": conflict["resolution_strategy"],
            "resolution_status": conflict["resolution_status"],
            "owner": conflict["owner"],
            "conflict_score": status_score(conflict["resolution_status"]),
        })

    consensus_rows = []
    for event in consensus:
        consensus_rows.append({
            "event_id": event["event_id"],
            "shard_id": event["shard_id"],
            "event_type": event["event_type"],
            "term": event["term"],
            "leader_node": event["leader_node"],
            "result": event["result"],
            "consensus_score": status_score(event["result"]),
            "notes": event["notes"],
        })

    failover_rows = []
    for drill in failovers:
        recovery = float(drill["recovery_time_seconds"])
        recovery_score = max(0.0, 1.0 - min(recovery / 300.0, 1.0))
        no_loss = 1.0 if drill["data_loss_observed"] == "0" else 0.0
        failover_rows.append({
            "drill_id": drill["drill_id"],
            "scenario": drill["scenario"],
            "affected_shard": drill["affected_shard"],
            "primary_node": drill["primary_node"],
            "replacement_node": drill["replacement_node"],
            "recovery_time_seconds": recovery,
            "data_loss_observed": drill["data_loss_observed"],
            "drill_status": drill["drill_status"],
            "failover_score": round(0.45 * recovery_score + 0.35 * no_loss + 0.20 * status_score(drill["drill_status"]), 3),
        })

    node_rows = []
    for node in nodes:
        cpu = float(node["cpu_utilization"])
        rtt = float(node["network_rtt_ms"])
        heartbeat_age = (datetime(2026, 5, 11, 10, 0, 10, tzinfo=timezone.utc) - parse_ts(node["last_heartbeat"])).total_seconds()
        resource_score = max(0.0, 1.0 - max(cpu - 0.70, 0) / 0.30)
        rtt_score = max(0.0, 1.0 - min(rtt / 150.0, 1.0))
        heartbeat_score = max(0.0, 1.0 - min(heartbeat_age / 60.0, 1.0))
        node_rows.append({
            "node_id": node["node_id"],
            "region": node["region"],
            "zone": node["zone"],
            "role": node["role"],
            "status": node["status"],
            "cpu_utilization": cpu,
            "network_rtt_ms": rtt,
            "heartbeat_age_seconds": round(heartbeat_age, 3),
            "node_score": round(0.30 * status_score(node["status"]) + 0.25 * resource_score + 0.25 * rtt_score + 0.20 * heartbeat_score, 3),
        })

    readiness = round(
        0.16 * mean([row["node_score"] for row in node_rows])
        + 0.16 * mean([row["shard_health_score"] for row in shard_rows])
        + 0.16 * mean([row["policy_score"] for row in quorum_rows])
        + 0.14 * mean([row["operation_score"] for row in operation_rows])
        + 0.12 * mean([row["conflict_score"] for row in conflict_rows])
        + 0.12 * mean([row["consensus_score"] for row in consensus_rows])
        + 0.14 * mean([row["failover_score"] for row in failover_rows]),
        3,
    )

    readiness_rows = [{
        "evaluation_run_id": run_id,
        "node_count": len(nodes),
        "shard_count": len(shards),
        "replica_count": len(replicas),
        "quorum_policy_count": len(policies),
        "operation_count": len(operations),
        "conflict_count": len(conflicts),
        "consensus_event_count": len(consensus),
        "failover_drill_count": len(failovers),
        "node_score": round(mean([row["node_score"] for row in node_rows]), 3),
        "shard_health_score": round(mean([row["shard_health_score"] for row in shard_rows]), 3),
        "quorum_policy_score": round(mean([row["policy_score"] for row in quorum_rows]), 3),
        "operation_score": round(mean([row["operation_score"] for row in operation_rows]), 3),
        "conflict_resolution_score": round(mean([row["conflict_score"] for row in conflict_rows]), 3),
        "consensus_score": round(mean([row["consensus_score"] for row in consensus_rows]), 3),
        "failover_score": round(mean([row["failover_score"] for row in failover_rows]), 3),
        "distributed_readiness_score": readiness,
        "distributed_readiness_gap": round(1.0 - readiness, 3),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Distributed Data Systems",
        "workflow": "distributed-data-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "cluster_nodes": {"path": str(nodes_path), "sha256": sha256_file(nodes_path), "rows": len(nodes)},
            "shard_map": {"path": str(shards_path), "sha256": sha256_file(shards_path), "rows": len(shards)},
            "replica_status": {"path": str(replicas_path), "sha256": sha256_file(replicas_path), "rows": len(replicas)},
            "quorum_policies": {"path": str(policies_path), "sha256": sha256_file(policies_path), "rows": len(policies)},
            "operation_log": {"path": str(operations_path), "sha256": sha256_file(operations_path), "rows": len(operations)},
            "conflict_records": {"path": str(conflicts_path), "sha256": sha256_file(conflicts_path), "rows": len(conflicts)},
            "consensus_events": {"path": str(consensus_path), "sha256": sha256_file(consensus_path), "rows": len(consensus)},
            "failover_drills": {"path": str(failover_path), "sha256": sha256_file(failover_path), "rows": len(failovers)},
        },
    }

    write_csv(ROOT / "outputs" / "shard_routing_examples_python.csv", routing_rows)
    write_csv(ROOT / "outputs" / "quorum_policy_scorecard_python.csv", quorum_rows)
    write_csv(ROOT / "outputs" / "shard_health_scorecard_python.csv", shard_rows)
    write_csv(ROOT / "outputs" / "operation_health_python.csv", operation_rows)
    write_csv(ROOT / "outputs" / "conflict_resolution_scorecard_python.csv", conflict_rows)
    write_csv(ROOT / "outputs" / "consensus_event_scorecard_python.csv", consensus_rows)
    write_csv(ROOT / "outputs" / "failover_drill_scorecard_python.csv", failover_rows)
    write_csv(ROOT / "outputs" / "node_health_scorecard_python.csv", node_rows)
    write_csv(ROOT / "outputs" / "distributed_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "distributed_data_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Distributed data systems scorecard complete")
    print(json.dumps({"nodes": len(nodes), "shards": len(shards), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
