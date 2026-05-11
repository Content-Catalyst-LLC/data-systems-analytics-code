#!/usr/bin/env python3
"""
Python Workflow: Data Quality and Observability Scorecard

This workflow evaluates datasets, quality checks, observability signals,
baselines, incidents, and lineage impact as a connected assurance system.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path.cwd()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def status_score(status: str) -> float:
    return {"pass": 1.0, "normal": 1.0, "warn": 0.6, "triggered": 0.4, "fail": 0.0}.get(status, 0.0)


def certification_score(status: str) -> float:
    return {"certified": 1.0, "reviewed": 0.7, "uncertified": 0.2}.get(status, 0.0)


def criticality_weight(criticality: str) -> float:
    return {"high": 1.0, "medium": 0.7, "low": 0.4}.get(criticality, 0.5)


def main() -> None:
    registry_path = ROOT / "data" / "dataset_registry.csv"
    checks_path = ROOT / "data" / "quality_checks.csv"
    events_path = ROOT / "data" / "observability_events.csv"
    baselines_path = ROOT / "data" / "baselines.csv"
    incidents_path = ROOT / "data" / "incidents.csv"
    lineage_path = ROOT / "data" / "lineage_impact.csv"

    registry = read_csv(registry_path)
    checks = read_csv(checks_path)
    events = read_csv(events_path)
    baselines = read_csv(baselines_path)
    incidents = read_csv(incidents_path)
    lineage = read_csv(lineage_path)

    checks_by_dataset = defaultdict(list)
    for row in checks:
        checks_by_dataset[row["dataset_id"]].append(status_score(row["status"]))

    events_by_dataset = defaultdict(list)
    for row in events:
        events_by_dataset[row["dataset_id"]].append(status_score(row["alert_status"]))

    incidents_by_dataset = defaultdict(list)
    for row in incidents:
        incidents_by_dataset[row["dataset_id"]].append(row)

    lineage_by_dataset = defaultdict(list)
    for row in lineage:
        lineage_by_dataset[row["upstream_dataset"]].append(row)

    baselines_by_dataset = defaultdict(list)
    for row in baselines:
        baselines_by_dataset[row["dataset_id"]].append(row)

    dataset_rows = []
    for ds in registry:
        dataset_id = ds["dataset_id"]
        quality_scores = checks_by_dataset.get(dataset_id, [])
        event_scores = events_by_dataset.get(dataset_id, [])
        dataset_incidents = incidents_by_dataset.get(dataset_id, [])

        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        avg_observability = sum(event_scores) / len(event_scores) if event_scores else 0.7
        baseline_coverage = min(len(baselines_by_dataset.get(dataset_id, [])) / 3.0, 1.0)
        lineage_coverage = 1.0 if lineage_by_dataset.get(dataset_id) else 0.0
        open_incidents = sum(1 for i in dataset_incidents if i["status"] != "resolved")
        incident_penalty = min(open_incidents * 0.2, 0.5)
        certified = certification_score(ds["certification_status"])

        reliability_score = round(
            max(
                0.0,
                0.30 * avg_quality
                + 0.20 * avg_observability
                + 0.15 * baseline_coverage
                + 0.15 * lineage_coverage
                + 0.10 * certified
                + 0.10 * (1.0 - incident_penalty),
            ),
            3,
        )

        trust_risk = round(
            criticality_weight(ds["criticality"]) * (1.0 - reliability_score),
            3,
        )

        dataset_rows.append({
            "dataset_id": dataset_id,
            "dataset_name": ds["dataset_name"],
            "domain": ds["domain"],
            "criticality": ds["criticality"],
            "certification_status": ds["certification_status"],
            "quality_score": round(avg_quality, 3),
            "observability_score": round(avg_observability, 3),
            "baseline_coverage": round(baseline_coverage, 3),
            "lineage_coverage": lineage_coverage,
            "open_incidents": open_incidents,
            "reliability_score": reliability_score,
            "trust_risk": trust_risk,
        })

    incident_rows = []
    for row in incidents:
        time_to_resolve = float(row["time_to_resolve_hours"])
        resolved = row["status"] == "resolved"
        incident_rows.append({
            "incident_id": row["incident_id"],
            "dataset_id": row["dataset_id"],
            "severity": row["severity"],
            "status": row["status"],
            "root_cause_category": row["root_cause_category"],
            "time_to_ack_hours": row["time_to_ack_hours"],
            "time_to_resolve_hours": row["time_to_resolve_hours"],
            "resolved": resolved,
            "consumer_notified": row["consumer_notified"],
            "remediation_score": round(1.0 if resolved and time_to_resolve <= 24 else 0.5 if resolved else 0.2, 3),
        })

    dimension_rows = [
        {"quality_dimension": dim, "check_count": count}
        for dim, count in sorted(Counter(c["quality_dimension"] for c in checks).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Quality Metrics and Observability",
        "workflow": "quality-observability-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "dataset_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "quality_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "observability_events": {"path": str(events_path), "sha256": sha256_file(events_path), "rows": len(events)},
            "baselines": {"path": str(baselines_path), "sha256": sha256_file(baselines_path), "rows": len(baselines)},
            "incidents": {"path": str(incidents_path), "sha256": sha256_file(incidents_path), "rows": len(incidents)},
            "lineage_impact": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
        },
        "outputs": {
            "dataset_scorecard": "outputs/dataset_quality_observability_scorecard_python.csv",
            "incident_review": "outputs/quality_incident_review_python.csv",
            "dimension_summary": "outputs/quality_dimension_summary_python.csv",
            "manifest": "outputs/quality_observability_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "dataset_quality_observability_scorecard_python.csv", dataset_rows)
    write_csv(ROOT / "outputs" / "quality_incident_review_python.csv", incident_rows)
    write_csv(ROOT / "outputs" / "quality_dimension_summary_python.csv", dimension_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "quality_observability_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Data quality and observability scorecard complete")
    print(json.dumps({
        "datasets": len(registry),
        "checks": len(checks),
        "observability_events": len(events),
        "incidents": len(incidents),
        "lineage_edges": len(lineage),
    }, indent=2))


if __name__ == "__main__":
    main()
