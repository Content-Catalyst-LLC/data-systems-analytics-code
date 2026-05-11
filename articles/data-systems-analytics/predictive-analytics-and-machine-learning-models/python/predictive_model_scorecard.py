#!/usr/bin/env python3
"""
Python Workflow: Predictive Analytics and Machine Learning Scorecard

This workflow evaluates predictive models across task definition, split design,
classification metrics, regression metrics, calibration, threshold policy,
leakage controls, monitoring windows, and governance status using only the
Python standard library.
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


def bool_value(value: str) -> bool:
    return value.strip().lower() == "true"


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "aligned": 1.0,
        "in_review": 0.7,
        "watch": 0.55,
        "planned": 0.45,
        "escalate": 0.25,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)


def confusion(y_true: list[int], scores: list[float], threshold: float) -> dict[str, int]:
    y_pred = [1 if s >= threshold else 0 for s in scores]
    return {
        "tp": sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 1),
        "fp": sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 1),
        "tn": sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 0),
        "fn": sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 0),
    }


def threshold_metrics(y_true: list[int], scores: list[float], threshold: float) -> dict[str, float]:
    c = confusion(y_true, scores, threshold)
    tp, fp, tn, fn = c["tp"], c["fp"], c["tn"], c["fn"]
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    accuracy = safe_div(tp + tn, tp + fp + tn + fn)
    f1 = safe_div(2 * precision * recall, precision + recall)
    return {
        **c,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": f1,
        "false_positive_rate": 1 - specificity,
        "false_negative_rate": 1 - recall,
    }


def roc_auc(y_true: list[int], scores: list[float]) -> float:
    positives = [s for y, s in zip(y_true, scores) if y == 1]
    negatives = [s for y, s in zip(y_true, scores) if y == 0]
    if not positives or not negatives:
        return 0.0
    wins = 0.0
    for ps in positives:
        for ns in negatives:
            wins += 1.0 if ps > ns else 0.5 if ps == ns else 0.0
    return wins / (len(positives) * len(negatives))


def brier_score(y_true: list[int], scores: list[float]) -> float:
    return sum((s - y) ** 2 for y, s in zip(y_true, scores)) / len(y_true)


def log_loss(y_true: list[int], scores: list[float], eps: float = 1e-15) -> float:
    clipped = [min(max(s, eps), 1 - eps) for s in scores]
    return -sum(y * math.log(s) + (1 - y) * math.log(1 - s) for y, s in zip(y_true, clipped)) / len(y_true)


def average_precision(y_true: list[int], scores: list[float]) -> float:
    ranked = sorted(zip(scores, y_true), reverse=True)
    positives = sum(y_true)
    if positives == 0:
        return 0.0
    tp = 0
    precision_sum = 0.0
    for rank, (_, y) in enumerate(ranked, start=1):
        if y == 1:
            tp += 1
            precision_sum += tp / rank
    return precision_sum / positives


def calibration_bins(y_true: list[int], scores: list[float], bins: int = 5) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for b in range(bins):
        lower = b / bins
        upper = (b + 1) / bins
        selected = [(y, s) for y, s in zip(y_true, scores) if lower <= s < upper or (b == bins - 1 and s == 1.0)]
        if not selected:
            continue
        ys = [y for y, _ in selected]
        ss = [s for _, s in selected]
        rows.append({
            "bin": b + 1,
            "lower": lower,
            "upper": upper,
            "count": len(selected),
            "mean_score": sum(ss) / len(ss),
            "observed_rate": sum(ys) / len(ys),
            "absolute_calibration_gap": abs((sum(ss) / len(ss)) - (sum(ys) / len(ys))),
        })
    return rows


def regression_metrics(y_true: list[float], y_pred: list[float]) -> dict[str, float]:
    errors = [pred - actual for actual, pred in zip(y_true, y_pred)]
    abs_errors = [abs(e) for e in errors]
    sq_errors = [e ** 2 for e in errors]
    sorted_abs = sorted(abs_errors)
    p90_index = min(len(sorted_abs) - 1, math.ceil(0.90 * len(sorted_abs)) - 1)
    mean_y = sum(y_true) / len(y_true)
    ss_res = sum(sq_errors)
    ss_tot = sum((y - mean_y) ** 2 for y in y_true)
    return {
        "mae": sum(abs_errors) / len(abs_errors),
        "rmse": math.sqrt(sum(sq_errors) / len(sq_errors)),
        "bias": sum(errors) / len(errors),
        "tail_error_p90": sorted_abs[p90_index],
        "r2": 1 - safe_div(ss_res, ss_tot),
    }


def split_score(row: dict[str, str]) -> float:
    protected = 1.0 if bool_value(row["test_set_protected"]) else 0.0
    strategy = 1.0 if row["split_strategy"] in {"stratified_random", "nested_stratified_kfold", "time_series_split", "grouped_temporal_split"} else 0.4
    structure = max(bool_value(row["stratified"]), bool_value(row["time_ordered"]), bool_value(row["group_aware"])) * 1.0
    return round(0.40 * protected + 0.35 * strategy + 0.15 * structure + 0.10 * status_score(row["status"]), 3)


def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.50}.get(value, 0.1)


def main() -> None:
    registry_path = ROOT / "data" / "model_registry.csv"
    classification_path = ROOT / "data" / "classification_predictions.csv"
    regression_path = ROOT / "data" / "regression_predictions.csv"
    splits_path = ROOT / "data" / "training_validation_splits.csv"
    thresholds_path = ROOT / "data" / "threshold_policies.csv"
    metrics_path = ROOT / "data" / "metric_scorecard.csv"
    checks_path = ROOT / "data" / "leakage_shift_checks.csv"
    monitoring_path = ROOT / "data" / "monitoring_windows.csv"

    registry = read_csv(registry_path)
    classification = read_csv(classification_path)
    regression = read_csv(regression_path)
    splits = read_csv(splits_path)
    thresholds = read_csv(thresholds_path)
    metric_scorecard = read_csv(metrics_path)
    checks = read_csv(checks_path)
    monitoring = read_csv(monitoring_path)

    classification_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in classification:
        classification_by_model[row["model_id"]].append(row)

    regression_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in regression:
        regression_by_model[row["model_id"]].append(row)

    split_by_model = {row["model_id"]: row for row in splits}

    checks_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in checks:
        checks_by_model[row["model_id"]].append(row)

    monitoring_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in monitoring:
        monitoring_by_model[row["model_id"]].append(row)

    classification_summary: list[dict[str, object]] = []
    threshold_rows: list[dict[str, object]] = []
    calibration_rows: list[dict[str, object]] = []
    subgroup_rows: list[dict[str, object]] = []
    regression_rows: list[dict[str, object]] = []
    governance_rows: list[dict[str, object]] = []
    monitoring_rows: list[dict[str, object]] = []

    for model in registry:
        model_id = model["model_id"]

        classification_score = 0.5
        calibration_score = 0.5
        threshold_policy_score = 0.5
        regression_score = 0.5

        if model_id in classification_by_model:
            rows = classification_by_model[model_id]
            y_true = [int(r["y_true"]) for r in rows]
            scores = [float(r["y_score"]) for r in rows]
            auc = roc_auc(y_true, scores)
            ap = average_precision(y_true, scores)
            brier = brier_score(y_true, scores)
            ll = log_loss(y_true, scores)
            classification_score = max(0.0, min(1.0, 0.55 * auc + 0.30 * ap + 0.15 * (1.0 - min(brier, 1.0))))
            calibration_score = max(0.0, min(1.0, 1.0 - brier))

            classification_summary.append({
                "model_id": model_id,
                "n": len(rows),
                "positive_rate": round(sum(y_true) / len(y_true), 4),
                "roc_auc": round(auc, 4),
                "average_precision": round(ap, 4),
                "brier_score": round(brier, 4),
                "log_loss": round(ll, 4),
                "classification_score": round(classification_score, 3),
                "calibration_score": round(calibration_score, 3),
            })

            model_thresholds = [t for t in thresholds if t["model_id"] == model_id]
            policy_scores = []
            for threshold_policy in model_thresholds:
                threshold = float(threshold_policy["threshold"])
                m = threshold_metrics(y_true, scores, threshold)
                expected_cost = (
                    m["fp"] * float(threshold_policy["false_positive_cost"])
                    + m["fn"] * float(threshold_policy["false_negative_cost"])
                )
                policy_score = 0.35 * m["precision"] + 0.35 * m["recall"] + 0.30 * status_score(threshold_policy["review_status"])
                policy_scores.append(policy_score)
                threshold_rows.append({
                    "model_id": model_id,
                    "policy_id": threshold_policy["policy_id"],
                    "threshold": threshold,
                    "policy_name": threshold_policy["policy_name"],
                    **{k: round(v, 4) if isinstance(v, float) else v for k, v in m.items()},
                    "expected_error_cost": round(expected_cost, 4),
                    "policy_score": round(policy_score, 3),
                })
            threshold_policy_score = statistics.mean(policy_scores) if policy_scores else 0.5

            for cal in calibration_bins(y_true, scores):
                calibration_rows.append({"model_id": model_id, **{k: round(v, 4) if isinstance(v, float) else v for k, v in cal.items()}})

            by_subgroup = defaultdict(list)
            for row in rows:
                by_subgroup[row["subgroup"]].append(row)
            for subgroup, subgroup_rows_model in by_subgroup.items():
                sy = [int(r["y_true"]) for r in subgroup_rows_model]
                ss = [float(r["y_score"]) for r in subgroup_rows_model]
                tm = threshold_metrics(sy, ss, 0.5)
                subgroup_rows.append({
                    "model_id": model_id,
                    "subgroup": subgroup,
                    "n": len(subgroup_rows_model),
                    "positive_rate": round(sum(sy) / len(sy), 4),
                    "precision_at_0_5": round(tm["precision"], 4),
                    "recall_at_0_5": round(tm["recall"], 4),
                    "accuracy_at_0_5": round(tm["accuracy"], 4),
                    "brier_score": round(brier_score(sy, ss), 4),
                })

        if model_id in regression_by_model:
            rows = regression_by_model[model_id]
            y_true = [float(r["y_true"]) for r in rows]
            y_pred = [float(r["y_pred"]) for r in rows]
            m = regression_metrics(y_true, y_pred)
            regression_score = max(0.0, min(1.0, 1.0 - (m["mae"] / max(sum(y_true) / len(y_true), 1.0))))
            regression_rows.append({
                "model_id": model_id,
                **{k: round(v, 4) for k, v in m.items()},
                "regression_score": round(regression_score, 3),
            })

        split_integrity = split_score(split_by_model.get(model_id, {
            "test_set_protected": "false",
            "split_strategy": "unknown",
            "stratified": "false",
            "time_ordered": "false",
            "group_aware": "false",
            "status": "needs_revision",
        }))

        model_checks = checks_by_model[model_id]
        check_scores = []
        for check in model_checks:
            base = {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(check["status"], 0.5)
            check_scores.append(max(0.0, base - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0)))
        leakage_shift_score = statistics.mean(check_scores) if check_scores else 0.45

        model_windows = monitoring_by_model[model_id]
        monitor_scores = []
        for window in model_windows:
            drift = float(window["drift_index"])
            score = max(0.0, status_score(window["status"]) - max(0.0, drift - 0.10))
            monitor_scores.append(score)
            monitoring_rows.append({
                **window,
                "monitoring_score": round(score, 3),
            })
        monitoring_score = statistics.mean(monitor_scores) if monitor_scores else 0.4

        scorecard_statuses = [m for m in metric_scorecard if m["model_id"] == model_id]
        metric_scores = [status_score(m["status"]) for m in scorecard_statuses]
        metric_governance = statistics.mean(metric_scores) if metric_scores else 0.4

        predictive_readiness = round(
            0.15 * status_score(model["status"])
            + 0.13 * split_integrity
            + 0.14 * classification_score
            + 0.12 * calibration_score
            + 0.12 * threshold_policy_score
            + 0.10 * regression_score
            + 0.10 * leakage_shift_score
            + 0.08 * metric_governance
            + 0.06 * monitoring_score,
            3,
        )

        governance_rows.append({
            "model_id": model_id,
            "model_name": model["model_name"],
            "task_type": model["task_type"],
            "model_family": model["model_family"],
            "status": model["status"],
            "risk_level": model["risk_level"],
            "split_integrity": round(split_integrity, 3),
            "classification_score": round(classification_score, 3),
            "calibration_score": round(calibration_score, 3),
            "threshold_policy_score": round(threshold_policy_score, 3),
            "regression_score": round(regression_score, 3),
            "leakage_shift_score": round(leakage_shift_score, 3),
            "metric_governance": round(metric_governance, 3),
            "monitoring_score": round(monitoring_score, 3),
            "predictive_readiness_score": predictive_readiness,
            "predictive_readiness_gap": round(1.0 - predictive_readiness, 3),
        })

    task_summary = [
        {"task_type": task, "model_count": count}
        for task, count in sorted(Counter(row["task_type"] for row in registry).items())
    ]
    family_summary = [
        {"model_family": family, "model_count": count}
        for family, count in sorted(Counter(row["model_family"] for row in registry).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Predictive Analytics and Machine Learning Models",
        "workflow": "predictive-model-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "model_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "classification_predictions": {"path": str(classification_path), "sha256": sha256_file(classification_path), "rows": len(classification)},
            "regression_predictions": {"path": str(regression_path), "sha256": sha256_file(regression_path), "rows": len(regression)},
            "training_validation_splits": {"path": str(splits_path), "sha256": sha256_file(splits_path), "rows": len(splits)},
            "threshold_policies": {"path": str(thresholds_path), "sha256": sha256_file(thresholds_path), "rows": len(thresholds)},
            "metric_scorecard": {"path": str(metrics_path), "sha256": sha256_file(metrics_path), "rows": len(metric_scorecard)},
            "leakage_shift_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "monitoring_windows": {"path": str(monitoring_path), "sha256": sha256_file(monitoring_path), "rows": len(monitoring)},
        },
        "outputs": {
            "predictive_readiness": "outputs/predictive_readiness_scorecard_python.csv",
            "classification_summary": "outputs/classification_summary_python.csv",
            "threshold_summary": "outputs/threshold_policy_summary_python.csv",
            "calibration_bins": "outputs/calibration_bins_python.csv",
            "subgroup_summary": "outputs/subgroup_summary_python.csv",
            "regression_summary": "outputs/regression_summary_python.csv",
            "monitoring_summary": "outputs/monitoring_summary_python.csv",
            "task_summary": "outputs/task_summary_python.csv",
            "family_summary": "outputs/model_family_summary_python.csv",
            "manifest": "outputs/predictive_model_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "predictive_readiness_scorecard_python.csv", governance_rows)
    write_csv(ROOT / "outputs" / "classification_summary_python.csv", classification_summary)
    write_csv(ROOT / "outputs" / "threshold_policy_summary_python.csv", threshold_rows)
    write_csv(ROOT / "outputs" / "calibration_bins_python.csv", calibration_rows)
    write_csv(ROOT / "outputs" / "subgroup_summary_python.csv", subgroup_rows)
    write_csv(ROOT / "outputs" / "regression_summary_python.csv", regression_rows)
    write_csv(ROOT / "outputs" / "monitoring_summary_python.csv", monitoring_rows)
    write_csv(ROOT / "outputs" / "task_summary_python.csv", task_summary)
    write_csv(ROOT / "outputs" / "model_family_summary_python.csv", family_summary)
    (ROOT / "outputs" / "predictive_model_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Predictive analytics scorecard complete")
    print(json.dumps({
        "models": len(registry),
        "classification_predictions": len(classification),
        "regression_predictions": len(regression),
        "threshold_policies": len(thresholds),
        "monitoring_windows": len(monitoring),
    }, indent=2))


if __name__ == "__main__":
    main()
