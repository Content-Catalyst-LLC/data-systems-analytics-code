#!/usr/bin/env python3
"""
Python Workflow: Semantic Layer Trust and Analytics Engineering Scorecard

This workflow evaluates semantic metrics and analytics models using certification,
quality tests, lineage visibility, grain discipline, usage, and definition-drift signals.
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


def certification_score(status: str) -> float:
    return {"certified": 1.0, "reviewed": 0.7, "uncertified": 0.2}.get(status, 0.0)


def test_status_score(status: str) -> float:
    return {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(status, 0.0)


def drift_score(local_definition_count: int) -> float:
    return round(1.0 / (1.0 + local_definition_count), 3)


def main() -> None:
    models_path = ROOT / "data" / "model_registry.csv"
    metrics_path = ROOT / "data" / "semantic_metrics.csv"
    tests_path = ROOT / "data" / "model_tests.csv"
    lineage_path = ROOT / "data" / "semantic_lineage.csv"
    usage_path = ROOT / "data" / "metric_usage.csv"
    drift_path = ROOT / "data" / "definition_drift.csv"

    models = read_csv(models_path)
    metrics = read_csv(metrics_path)
    tests = read_csv(tests_path)
    lineage = read_csv(lineage_path)
    usage = read_csv(usage_path)
    drift = read_csv(drift_path)

    tests_by_model = defaultdict(list)
    for row in tests:
        tests_by_model[row["model_id"]].append(test_status_score(row["status"]))

    upstream_edges = Counter(row["downstream_model"] for row in lineage)
    downstream_edges = Counter(row["upstream_model"] for row in lineage)

    usage_by_metric = defaultdict(lambda: {"query_count": 0, "dashboard_views": 0, "notebook_sessions": 0})
    for row in usage:
        metric_usage = usage_by_metric[row["metric_id"]]
        metric_usage["query_count"] += int(row["query_count"])
        metric_usage["dashboard_views"] += int(row["dashboard_views"])
        metric_usage["notebook_sessions"] += int(row["notebook_sessions"])

    drift_by_metric_name = {row["metric_name"]: row for row in drift}

    model_rows = []
    for model in models:
        test_scores = tests_by_model.get(model["model_id"], [])
        avg_test_score = sum(test_scores) / len(test_scores) if test_scores else 0.0
        has_lineage = 1.0 if upstream_edges[model["model_id"]] or downstream_edges[model["model_id"]] else 0.0
        grain_score = 0.0 if model["grain"] in {"", "mixed"} else 1.0
        lifecycle_score = {"active": 1.0, "beta": 0.7, "deprecated": 0.2}.get(model["lifecycle_status"], 0.5)

        readiness = round(
            0.35 * avg_test_score
            + 0.25 * has_lineage
            + 0.20 * grain_score
            + 0.20 * lifecycle_score,
            3,
        )

        model_rows.append({
            "model_id": model["model_id"],
            "model_name": model["model_name"],
            "layer": model["layer"],
            "domain": model["domain"],
            "grain": model["grain"],
            "lifecycle_status": model["lifecycle_status"],
            "average_test_score": round(avg_test_score, 3),
            "lineage_present": has_lineage,
            "model_readiness_score": readiness,
        })

    metric_rows = []
    for metric in metrics:
        usage_values = usage_by_metric[metric["metric_id"]]
        total_usage = sum(usage_values.values())
        normalized_usage = min(total_usage / 500.0, 1.0)
        drift_record = drift_by_metric_name.get(metric["metric_name"])
        local_defs = int(drift_record["local_definition_count"]) if drift_record else 0
        consistency = drift_score(local_defs)
        lineage_present = 1.0 if any(row["downstream_model"] == metric["base_model"] or row["upstream_model"] == metric["base_model"] for row in lineage) else 0.0

        semantic_trust = round(
            0.30 * certification_score(metric["certification_status"])
            + 0.20 * consistency
            + 0.20 * lineage_present
            + 0.15 * normalized_usage
            + 0.15 * (1.0 if metric["grain"] not in {"", "mixed"} else 0.0),
            3,
        )

        metric_rows.append({
            "metric_id": metric["metric_id"],
            "metric_name": metric["metric_name"],
            "domain": metric["domain"],
            "owner": metric["owner"],
            "certification_status": metric["certification_status"],
            "version": metric["version"],
            "local_definition_count": local_defs,
            "semantic_consistency_score": consistency,
            "total_usage": total_usage,
            "semantic_trust_score": semantic_trust,
        })

    domain_rows = []
    trust_by_domain = defaultdict(list)
    for row in metric_rows:
        trust_by_domain[str(row["domain"])].append(float(row["semantic_trust_score"]))
    for domain, values in sorted(trust_by_domain.items()):
        domain_rows.append({
            "domain": domain,
            "metric_count": len(values),
            "average_semantic_trust_score": round(sum(values) / len(values), 3),
        })

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Analytics Engineering and Semantic Layers",
        "workflow": "semantic-layer-trust-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "model_registry": {"path": str(models_path), "sha256": sha256_file(models_path), "rows": len(models)},
            "semantic_metrics": {"path": str(metrics_path), "sha256": sha256_file(metrics_path), "rows": len(metrics)},
            "model_tests": {"path": str(tests_path), "sha256": sha256_file(tests_path), "rows": len(tests)},
            "semantic_lineage": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
            "metric_usage": {"path": str(usage_path), "sha256": sha256_file(usage_path), "rows": len(usage)},
            "definition_drift": {"path": str(drift_path), "sha256": sha256_file(drift_path), "rows": len(drift)},
        },
        "outputs": {
            "model_scorecard": "outputs/model_readiness_scorecard_python.csv",
            "metric_scorecard": "outputs/semantic_metric_trust_scorecard_python.csv",
            "domain_summary": "outputs/domain_semantic_trust_summary_python.csv",
            "manifest": "outputs/semantic_layer_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "model_readiness_scorecard_python.csv", model_rows)
    write_csv(ROOT / "outputs" / "semantic_metric_trust_scorecard_python.csv", metric_rows)
    write_csv(ROOT / "outputs" / "domain_semantic_trust_summary_python.csv", domain_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "semantic_layer_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Semantic layer trust scorecard complete")
    print(json.dumps({
        "models": len(models),
        "metrics": len(metrics),
        "tests": len(tests),
        "lineage_edges": len(lineage),
        "usage_rows": len(usage),
    }, indent=2))


if __name__ == "__main__":
    main()
