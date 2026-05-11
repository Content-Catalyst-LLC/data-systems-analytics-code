#!/usr/bin/env python3
"""
Python Workflow: Feature Engineering and Data Representation Scorecard

This workflow creates example engineered features and evaluates representation
integrity using transformation rules, leakage checks, feature quality checks,
selection status, sparsity, OOV risk, and approval state.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
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


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def status_score(value: str) -> float:
    return {"approved": 1.0, "in_review": 0.7, "watch": 0.55, "planned": 0.45, "needs_revision": 0.15, "blocked_leakage": 0.0}.get(value, 0.5)


def leakage_score(value: str) -> float:
    return {"low": 1.0, "medium": 0.6, "high": 0.0}.get(value, 0.5)


def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.50}.get(value, 0.1)


def bool_value(value: str) -> bool:
    return value.strip().lower() == "true"


def main() -> None:
    raw_path = ROOT / "data" / "raw_observations.csv"
    registry_path = ROOT / "data" / "feature_registry.csv"
    rules_path = ROOT / "data" / "transformation_rules.csv"
    checks_path = ROOT / "data" / "feature_quality_checks.csv"
    selection_path = ROOT / "data" / "selection_scores.csv"
    representation_path = ROOT / "data" / "representation_metrics.csv"

    raw = read_csv(raw_path)
    registry = read_csv(registry_path)
    rules = read_csv(rules_path)
    checks = read_csv(checks_path)
    selection = read_csv(selection_path)
    representations = read_csv(representation_path)

    spend_values = [float(row["monthly_spend"]) for row in raw]
    events_values = [float(row["events_30d"]) for row in raw]
    events_mean = statistics.mean(events_values)
    events_sd = statistics.pstdev(events_values) or 1.0

    engineered_rows = []
    for row in raw:
        event_time = parse_dt(row["event_time"])
        signup_time = parse_dt(row["signup_time"])
        hour = event_time.hour
        engineered_rows.append({
            "entity_id": row["entity_id"],
            "label_churn": row["label_churn"],
            "log_monthly_spend": round(math.log1p(float(row["monthly_spend"])), 6),
            "events_30d_scaled": round((float(row["events_30d"]) - events_mean) / events_sd, 6),
            "days_since_last_event_bucket": (
                "0_7" if int(row["days_since_last_event"]) <= 7
                else "8_14" if int(row["days_since_last_event"]) <= 14
                else "15_plus"
            ),
            "region_one_hot_key": f"region={row['region']}",
            "channel_plan_cross": f"{row['channel']}__{row['plan_type']}",
            "event_hour_sin": round(math.sin(2 * math.pi * hour / 24), 6),
            "event_hour_cos": round(math.cos(2 * math.pi * hour / 24), 6),
            "tenure_days": (event_time - signup_time).days,
        })

    rules_by_feature = defaultdict(list)
    for row in rules:
        rules_by_feature[row["feature_id"]].append(row)

    checks_by_feature = defaultdict(list)
    for row in checks:
        checks_by_feature[row["feature_id"]].append(row)

    selection_by_feature = {row["feature_id"]: row for row in selection}

    feature_rows = []
    for feature in registry:
        feature_id = feature["feature_id"]
        feature_rules = rules_by_feature[feature_id]
        feature_checks = checks_by_feature[feature_id]
        selection_row = selection_by_feature.get(feature_id, {})

        rule_scores = []
        for rule in feature_rules:
            no_refit_leakage = 1.0 if rule["fit_scope"] in {"training_only", "no_fit"} else 0.0
            prediction_available = 1.0 if bool_value(rule["allowed_at_prediction_time"]) else 0.0
            rule_scores.append(0.4 * no_refit_leakage + 0.4 * prediction_available + 0.2 * status_score(rule["review_status"]))
        transformation_integrity = sum(rule_scores) / len(rule_scores) if rule_scores else 0.5

        check_scores = []
        for check in feature_checks:
            base = {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(check["status"], 0.5)
            check_scores.append(max(0.0, base - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0)))
        quality_integrity = sum(check_scores) / len(check_scores) if check_scores else 0.6

        selection_integrity = status_score(selection_row.get("selection_status", "watch"))
        representation_integrity = round(
            0.25 * status_score(feature["status"])
            + 0.25 * leakage_score(feature["leakage_risk"])
            + 0.25 * transformation_integrity
            + 0.15 * quality_integrity
            + 0.10 * selection_integrity,
            3,
        )

        feature_rows.append({
            "feature_id": feature_id,
            "feature_name": feature["feature_name"],
            "feature_family": feature["feature_family"],
            "status": feature["status"],
            "leakage_risk": feature["leakage_risk"],
            "interpretability": feature["interpretability"],
            "transformation_integrity": round(transformation_integrity, 3),
            "quality_integrity": round(quality_integrity, 3),
            "selection_integrity": round(selection_integrity, 3),
            "representation_integrity": representation_integrity,
            "representation_integrity_gap": round(1.0 - representation_integrity, 3),
        })

    representation_rows = []
    for row in representations:
        dimensionality_penalty = min(float(row["feature_count"]) / 200.0, 0.2)
        sparsity_penalty = max(0.0, float(row["sparsity_ratio"]) - 0.85) * 0.5
        leakage_penalty = int(row["leakage_flag_count"]) * 0.3
        score = max(
            0.0,
            0.45 * status_score(row["status"])
            + 0.35 * float(row["approved_feature_share"])
            + 0.20 * (1.0 - float(row["oov_rate"]))
            - dimensionality_penalty
            - sparsity_penalty
            - leakage_penalty,
        )
        representation_rows.append({
            **row,
            "representation_readiness_score": round(score, 3),
            "representation_readiness_gap": round(1.0 - score, 3),
        })

    family_rows = [
        {"feature_family": family, "feature_count": count}
        for family, count in sorted(Counter(f["feature_family"] for f in registry).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Feature Engineering and Data Representation",
        "workflow": "feature-engineering-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "raw_observations": {"path": str(raw_path), "sha256": sha256_file(raw_path), "rows": len(raw)},
            "feature_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "transformation_rules": {"path": str(rules_path), "sha256": sha256_file(rules_path), "rows": len(rules)},
            "feature_quality_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "selection_scores": {"path": str(selection_path), "sha256": sha256_file(selection_path), "rows": len(selection)},
            "representation_metrics": {"path": str(representation_path), "sha256": sha256_file(representation_path), "rows": len(representations)},
        },
        "outputs": {
            "engineered_features": "outputs/engineered_features_python.csv",
            "feature_integrity": "outputs/feature_integrity_scorecard_python.csv",
            "representation_readiness": "outputs/representation_readiness_python.csv",
            "feature_family_summary": "outputs/feature_family_summary_python.csv",
            "manifest": "outputs/feature_engineering_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "engineered_features_python.csv", engineered_rows)
    write_csv(ROOT / "outputs" / "feature_integrity_scorecard_python.csv", feature_rows)
    write_csv(ROOT / "outputs" / "representation_readiness_python.csv", representation_rows)
    write_csv(ROOT / "outputs" / "feature_family_summary_python.csv", family_rows)
    (ROOT / "outputs" / "feature_engineering_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Feature engineering scorecard complete")
    print(json.dumps({
        "raw_rows": len(raw),
        "features": len(registry),
        "rules": len(rules),
        "quality_checks": len(checks),
        "representations": len(representations),
    }, indent=2))


if __name__ == "__main__":
    main()
