#!/usr/bin/env python3
"""
Python Workflow: Pipeline DAG, Observability, Backfill, and Readiness Scorecard

This workflow evaluates pipeline stages, DAG edges, run health, quality gates,
observability metrics, lineage edges, backfill records, idempotency checks, and
pipeline-readiness scores using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import statistics
import sys
import uuid
from collections import Counter, defaultdict, deque
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

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "success": 1.0,
        "complete": 1.0,
        "completed": 1.0,
        "success_with_warning": 0.72,
        "completed_with_warning": 0.72,
        "in_review": 0.65,
        "partial": 0.55,
        "pending": 0.45,
        "warn": 0.40,
        "degraded": 0.25,
        "failed": 0.0,
    }.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.45}.get(value, 0.1)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def topological_sort(stages: list[dict[str, str]]) -> list[dict[str, object]]:
    by_pipeline = defaultdict(list)
    for stage in stages:
        by_pipeline[stage["pipeline_name"]].append(stage)

    rows = []
    for pipeline, pipeline_stages in sorted(by_pipeline.items()):
        nodes = {stage["stage_name"] for stage in pipeline_stages}
        indegree = {node: 0 for node in nodes}
        adjacency = defaultdict(list)

        for stage in pipeline_stages:
            upstream = stage["upstream_stage"].strip()
            if upstream:
                adjacency[upstream].append(stage["stage_name"])
                indegree[stage["stage_name"]] += 1

        queue = deque(sorted([node for node, degree in indegree.items() if degree == 0]))
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in sorted(adjacency[node]):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        is_acyclic = len(order) == len(nodes)
        rows.append({
            "pipeline_name": pipeline,
            "stage_count": len(nodes),
            "topological_order": " > ".join(order),
            "is_acyclic": int(is_acyclic),
            "root_stage_count": sum(1 for stage in pipeline_stages if not stage["upstream_stage"].strip()),
            "terminal_stage_count": sum(1 for stage in pipeline_stages if not stage["downstream_stage"].strip()),
        })

    return rows

def main() -> None:
    stages_path = ROOT / "data" / "pipeline_stages.csv"
    runs_path = ROOT / "data" / "pipeline_runs.csv"
    gates_path = ROOT / "data" / "quality_gates.csv"
    observability_path = ROOT / "data" / "observability_metrics.csv"
    lineage_path = ROOT / "data" / "lineage_edges.csv"
    backfill_path = ROOT / "data" / "backfill_requests.csv"
    idempotency_path = ROOT / "data" / "idempotency_checks.csv"

    stages = read_csv(stages_path)
    runs = read_csv(runs_path)
    gates = read_csv(gates_path)
    observability = read_csv(observability_path)
    lineage = read_csv(lineage_path)
    backfills = read_csv(backfill_path)
    idempotency = read_csv(idempotency_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()

    dag_rows = topological_sort(stages)

    stage_rows = []
    for stage in stages:
        score = max(
            0.0,
            status_score(stage["status"]) - (severity_penalty(stage["criticality"]) if stage["status"] != "approved" else 0.0),
        )
        stage_rows.append({
            "pipeline_name": stage["pipeline_name"],
            "stage_name": stage["stage_name"],
            "stage_type": stage["stage_type"],
            "mode": stage["mode"],
            "owner": stage["owner"],
            "criticality": stage["criticality"],
            "status": stage["status"],
            "stage_score": round(score, 3),
        })

    run_rows = []
    for run in runs:
        input_rows = float(run["input_rows"])
        output_rows = float(run["output_rows"])
        failed_rows = float(run["failed_rows"])
        duration_seconds = (
            datetime.fromisoformat(run["finished_at"].replace("Z", "+00:00"))
            - datetime.fromisoformat(run["started_at"].replace("Z", "+00:00"))
        ).total_seconds()
        run_rows.append({
            "run_id": run["run_id"],
            "pipeline_name": run["pipeline_name"],
            "run_mode": run["run_mode"],
            "duration_seconds": round(duration_seconds, 3),
            "input_rows": int(input_rows),
            "output_rows": int(output_rows),
            "failed_rows": int(failed_rows),
            "failure_rate": round(failed_rows / input_rows if input_rows else 0.0, 5),
            "retry_count": run["retry_count"],
            "status": run["status"],
            "run_score": status_score(run["status"]),
        })

    gate_rows = []
    for gate in gates:
        observed = float(gate["observed_value"])
        threshold = float(gate["threshold"])
        passed = observed >= threshold and gate["status"] == "pass"
        score = min(1.0, observed / threshold) if threshold else observed
        if gate["status"] != "pass":
            score = max(0.0, score - severity_penalty(gate["severity"]))
        gate_rows.append({
            "gate_id": gate["gate_id"],
            "pipeline_name": gate["pipeline_name"],
            "stage_name": gate["stage_name"],
            "dimension": gate["dimension"],
            "rule_name": gate["rule_name"],
            "threshold": threshold,
            "observed_value": observed,
            "passed": int(passed),
            "severity": gate["severity"],
            "status": gate["status"],
            "gate_score": round(score, 3),
        })

    obs_rows = []
    for obs in observability:
        latency = float(obs["latency_seconds"])
        lag = float(obs["lag_seconds"])
        error_rate = float(obs["error_rate"])
        watermark_lag = float(obs["watermark_lag_seconds"])
        backpressure = float(obs["backpressure_ms"])
        score = 1.0
        if latency > 900:
            score -= 0.15
        if lag > 60:
            score -= 0.20
        if error_rate > 0.005:
            score -= 0.20
        if watermark_lag > 60:
            score -= 0.15
        if backpressure > 100:
            score -= 0.15
        if obs["status"] != "pass":
            score -= 0.10
        obs_rows.append({
            "metric_id": obs["metric_id"],
            "pipeline_name": obs["pipeline_name"],
            "observed_at": obs["observed_at"],
            "throughput_rows_per_sec": obs["throughput_rows_per_sec"],
            "latency_seconds": latency,
            "lag_seconds": lag,
            "error_rate": error_rate,
            "watermark_lag_seconds": watermark_lag,
            "backpressure_ms": backpressure,
            "status": obs["status"],
            "observability_score": round(max(0.0, score), 3),
        })

    lineage_rows = []
    for edge in lineage:
        lineage_rows.append({
            "edge_id": edge["edge_id"],
            "pipeline_name": edge["pipeline_name"],
            "from_node": edge["from_node"],
            "to_node": edge["to_node"],
            "edge_type": edge["edge_type"],
            "records_moved": edge["records_moved"],
            "lineage_status": edge["lineage_status"],
            "lineage_score": status_score(edge["lineage_status"]),
        })

    backfill_rows = []
    for item in backfills:
        backfill_rows.append({
            "backfill_id": item["backfill_id"],
            "pipeline_name": item["pipeline_name"],
            "reason": item["reason"],
            "start_period": item["start_period"],
            "end_period": item["end_period"],
            "expected_rows": item["expected_rows"],
            "status": item["status"],
            "owner": item["owner"],
            "backfill_score": status_score(item["status"]),
        })

    idempotency_rows = []
    for check in idempotency:
        duplicate_effect = int(check["duplicate_effect_count"])
        first = int(check["first_output_rows"])
        second = int(check["second_output_rows"])
        stable_output = int(first == second and duplicate_effect == 0)
        score = 1.0 if stable_output and check["status"] == "pass" else max(0.0, 0.65 - min(0.5, duplicate_effect / max(first, 1)))
        idempotency_rows.append({
            "check_id": check["check_id"],
            "pipeline_name": check["pipeline_name"],
            "stage_name": check["stage_name"],
            "key_strategy": check["key_strategy"],
            "first_output_rows": first,
            "second_output_rows": second,
            "duplicate_effect_count": duplicate_effect,
            "stable_output": stable_output,
            "status": check["status"],
            "idempotency_score": round(score, 3),
        })

    readiness_rows = []
    pipeline_names = sorted({row["pipeline_name"] for row in stages})
    for pipeline in pipeline_names:
        stage_score = mean([row["stage_score"] for row in stage_rows if row["pipeline_name"] == pipeline])
        run_score = mean([row["run_score"] for row in run_rows if row["pipeline_name"] == pipeline])
        gate_score = mean([row["gate_score"] for row in gate_rows if row["pipeline_name"] == pipeline])
        obs_score = mean([row["observability_score"] for row in obs_rows if row["pipeline_name"] == pipeline])
        lineage_score = mean([row["lineage_score"] for row in lineage_rows if row["pipeline_name"] == pipeline])
        backfill_score = mean([row["backfill_score"] for row in backfill_rows if row["pipeline_name"] == pipeline])
        idempotency_score = mean([row["idempotency_score"] for row in idempotency_rows if row["pipeline_name"] == pipeline])
        dag_score = mean([row["is_acyclic"] for row in dag_rows if row["pipeline_name"] == pipeline])

        readiness = round(
            0.14 * dag_score
            + 0.14 * stage_score
            + 0.14 * run_score
            + 0.16 * gate_score
            + 0.14 * obs_score
            + 0.12 * lineage_score
            + 0.08 * backfill_score
            + 0.08 * idempotency_score,
            3,
        )
        readiness_rows.append({
            "evaluation_run_id": run_id,
            "pipeline_name": pipeline,
            "dag_score": round(dag_score, 3),
            "stage_score": round(stage_score, 3),
            "run_score": round(run_score, 3),
            "quality_gate_score": round(gate_score, 3),
            "observability_score": round(obs_score, 3),
            "lineage_score": round(lineage_score, 3),
            "backfill_score": round(backfill_score, 3),
            "idempotency_score": round(idempotency_score, 3),
            "pipeline_readiness_score": readiness,
            "pipeline_readiness_gap": round(1.0 - readiness, 3),
        })

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Data Pipelines and Data Processing Systems",
        "workflow": "pipeline-processing-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "pipeline_stages": {"path": str(stages_path), "sha256": sha256_file(stages_path), "rows": len(stages)},
            "pipeline_runs": {"path": str(runs_path), "sha256": sha256_file(runs_path), "rows": len(runs)},
            "quality_gates": {"path": str(gates_path), "sha256": sha256_file(gates_path), "rows": len(gates)},
            "observability_metrics": {"path": str(observability_path), "sha256": sha256_file(observability_path), "rows": len(observability)},
            "lineage_edges": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
            "backfill_requests": {"path": str(backfill_path), "sha256": sha256_file(backfill_path), "rows": len(backfills)},
            "idempotency_checks": {"path": str(idempotency_path), "sha256": sha256_file(idempotency_path), "rows": len(idempotency)},
        },
    }

    write_csv(ROOT / "outputs" / "dag_topology_python.csv", dag_rows)
    write_csv(ROOT / "outputs" / "stage_scorecard_python.csv", stage_rows)
    write_csv(ROOT / "outputs" / "pipeline_run_health_python.csv", run_rows)
    write_csv(ROOT / "outputs" / "quality_gate_scorecard_python.csv", gate_rows)
    write_csv(ROOT / "outputs" / "observability_scorecard_python.csv", obs_rows)
    write_csv(ROOT / "outputs" / "lineage_scorecard_python.csv", lineage_rows)
    write_csv(ROOT / "outputs" / "backfill_replay_scorecard_python.csv", backfill_rows)
    write_csv(ROOT / "outputs" / "idempotency_scorecard_python.csv", idempotency_rows)
    write_csv(ROOT / "outputs" / "pipeline_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "pipeline_processing_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Pipeline processing scorecard complete")
    print(json.dumps({"pipelines": len(pipeline_names), "readiness": readiness_rows}, indent=2))

if __name__ == "__main__":
    main()
