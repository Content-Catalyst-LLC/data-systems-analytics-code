#!/usr/bin/env python3
"""
Python Workflow: BI Decision-Support Scorecard

This workflow evaluates BI metrics and dashboards as decision-support assets.
It combines metric trust, semantic certification, freshness, uncertainty visibility,
dashboard certification, alert response, and decision traceability.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
import uuid
from collections import defaultdict
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
    return {
        "certified": 1.0,
        "reviewed": 0.7,
        "uncertified": 0.2,
    }.get(status, 0.0)


def lifecycle_score(status: str) -> float:
    return {
        "active": 1.0,
        "beta": 0.7,
        "deprecated": 0.2,
        "retired": 0.0,
    }.get(status, 0.5)


def main() -> None:
    metrics_path = ROOT / "data" / "bi_metrics.csv"
    dashboards_path = ROOT / "data" / "dashboard_inventory.csv"
    thresholds_path = ROOT / "data" / "decision_thresholds.csv"
    alerts_path = ROOT / "data" / "alert_events.csv"
    reviews_path = ROOT / "data" / "decision_reviews.csv"

    metrics = read_csv(metrics_path)
    dashboards = read_csv(dashboards_path)
    thresholds = read_csv(thresholds_path)
    alerts = read_csv(alerts_path)
    reviews = read_csv(reviews_path)

    metric_by_id = {row["metric_id"]: row for row in metrics}

    alert_response_by_dashboard: dict[str, list[float]] = defaultdict(list)
    for row in alerts:
        alert_response_by_dashboard[row["dashboard_id"]].append(float(row["time_to_acknowledge_hours"]))

    review_traceability: dict[str, list[bool]] = defaultdict(list)
    for row in reviews:
        review_traceability[row["dashboard_id"]].append(row["action_traceable"].lower() == "true")

    scorecard_rows: list[dict[str, object]] = []
    for dash in dashboards:
        related_alert_times = alert_response_by_dashboard.get(dash["dashboard_id"], [])
        avg_ack = sum(related_alert_times) / len(related_alert_times) if related_alert_times else None
        response_score = 1.0 if avg_ack is None else max(0.0, min(1.0, 1.0 - (avg_ack / 24.0)))

        trace_values = review_traceability.get(dash["dashboard_id"], [])
        trace_score = sum(trace_values) / len(trace_values) if trace_values else 0.0

        certification = status_score(dash["certification_status"])
        lifecycle = lifecycle_score(dash["lifecycle_status"])

        decision_support_score = round(
            0.30 * certification
            + 0.20 * lifecycle
            + 0.20 * response_score
            + 0.20 * trace_score
            + 0.10 * (1.0 if dash["decision_function"] else 0.0),
            3,
        )

        scorecard_rows.append({
            "dashboard_id": dash["dashboard_id"],
            "dashboard_name": dash["dashboard_name"],
            "domain": dash["domain"],
            "primary_user": dash["primary_user"],
            "decision_function": dash["decision_function"],
            "certification_status": dash["certification_status"],
            "lifecycle_status": dash["lifecycle_status"],
            "average_alert_ack_hours": "" if avg_ack is None else round(avg_ack, 2),
            "traceability_score": round(trace_score, 3),
            "decision_support_score": decision_support_score,
        })

    metric_rows = []
    for metric in metrics:
        metric_trust = round(
            0.45 * float(metric["quality_score"])
            + 0.25 * status_score(metric["semantic_status"])
            + 0.15 * (1.0 if metric["uncertainty_visible"].lower() == "true" else 0.0)
            + 0.15 * (1.0 if metric["decision_critical"].lower() == "true" else 0.7),
            3,
        )
        metric_rows.append({
            "metric_id": metric["metric_id"],
            "metric_name": metric["metric_name"],
            "domain": metric["domain"],
            "owner": metric["owner"],
            "semantic_status": metric["semantic_status"],
            "quality_score": metric["quality_score"],
            "uncertainty_visible": metric["uncertainty_visible"],
            "metric_trust_score": metric_trust,
        })

    domain_rows = []
    domain_scores: dict[str, list[float]] = defaultdict(list)
    for row in scorecard_rows:
        domain_scores[str(row["domain"])].append(float(row["decision_support_score"]))
    for domain, scores in sorted(domain_scores.items()):
        domain_rows.append({
            "domain": domain,
            "dashboard_count": len(scores),
            "average_decision_support_score": round(sum(scores) / len(scores), 3),
        })

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Business Intelligence Systems and Decision Support",
        "workflow": "bi-decision-support-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "bi_metrics": {"path": str(metrics_path), "sha256": sha256_file(metrics_path), "rows": len(metrics)},
            "dashboard_inventory": {"path": str(dashboards_path), "sha256": sha256_file(dashboards_path), "rows": len(dashboards)},
            "decision_thresholds": {"path": str(thresholds_path), "sha256": sha256_file(thresholds_path), "rows": len(thresholds)},
            "alert_events": {"path": str(alerts_path), "sha256": sha256_file(alerts_path), "rows": len(alerts)},
            "decision_reviews": {"path": str(reviews_path), "sha256": sha256_file(reviews_path), "rows": len(reviews)},
        },
        "outputs": {
            "dashboard_scorecard": "outputs/dashboard_decision_support_scorecard_python.csv",
            "metric_trust": "outputs/metric_trust_scorecard_python.csv",
            "domain_summary": "outputs/domain_decision_support_summary_python.csv",
            "manifest": "outputs/bi_decision_support_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "dashboard_decision_support_scorecard_python.csv", scorecard_rows)
    write_csv(ROOT / "outputs" / "metric_trust_scorecard_python.csv", metric_rows)
    write_csv(ROOT / "outputs" / "domain_decision_support_summary_python.csv", domain_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "bi_decision_support_manifest_python.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("BI decision-support scorecard complete")
    print(json.dumps({
        "metrics": len(metrics),
        "dashboards": len(dashboards),
        "thresholds": len(thresholds),
        "alerts": len(alerts),
        "reviews": len(reviews),
    }, indent=2))


if __name__ == "__main__":
    main()
