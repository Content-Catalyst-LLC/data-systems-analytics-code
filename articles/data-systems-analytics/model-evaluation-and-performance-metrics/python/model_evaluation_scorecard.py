#!/usr/bin/env python3
"""
Python Workflow: Model Evaluation and Performance Metrics Scorecard

This workflow evaluates binary classification, threshold policy, calibration,
regression error, subgroup behavior, monitoring windows, and governance limits
using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
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


def confusion(y_true: list[int], scores: list[float], threshold: float) -> dict[str, int]:
    y_pred = [1 if s >= threshold else 0 for s in scores]
    return {
        "tp": sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 1),
        "fp": sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 1),
        "tn": sum(1 for y, p in zip(y_true, y_pred) if y == 0 and p == 0),
        "fn": sum(1 for y, p in zip(y_true, y_pred) if y == 1 and p == 0),
    }


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


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
    pairs = [(score, y) for y, score in zip(y_true, scores)]
    positives = [score for score, y in pairs if y == 1]
    negatives = [score for score, y in pairs if y == 0]
    if not positives or not negatives:
        return 0.0
    wins = 0.0
    total = len(positives) * len(negatives)
    for ps in positives:
        for ns in negatives:
            if ps > ns:
                wins += 1.0
            elif ps == ns:
                wins += 0.5
    return wins / total


def brier_score(y_true: list[int], scores: list[float]) -> float:
    return sum((s - y) ** 2 for y, s in zip(y_true, scores)) / len(y_true)


def log_loss(y_true: list[int], scores: list[float], eps: float = 1e-15) -> float:
    clipped = [min(max(s, eps), 1 - eps) for s in scores]
    return -sum(y * math.log(s) + (1 - y) * math.log(1 - s) for y, s in zip(y_true, clipped)) / len(y_true)


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
        "mse": sum(sq_errors) / len(sq_errors),
        "bias": sum(errors) / len(errors),
        "tail_error_p90": sorted_abs[p90_index],
        "r2": 1 - safe_div(ss_res, ss_tot),
    }


def main() -> None:
    registry_path = ROOT / "data" / "model_registry.csv"
    binary_path = ROOT / "data" / "binary_predictions.csv"
    regression_path = ROOT / "data" / "regression_predictions.csv"
    thresholds_path = ROOT / "data" / "threshold_policies.csv"
    scorecard_path = ROOT / "data" / "metric_scorecard.csv"
    monitoring_path = ROOT / "data" / "monitoring_windows.csv"

    registry = read_csv(registry_path)
    binary = read_csv(binary_path)
    regression = read_csv(regression_path)
    thresholds = read_csv(thresholds_path)
    scorecard = read_csv(scorecard_path)
    monitoring = read_csv(monitoring_path)

    binary_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in binary:
        binary_by_model[row["model_id"]].append(row)

    threshold_rows: list[dict[str, object]] = []
    calibration_rows: list[dict[str, object]] = []
    model_summary_rows: list[dict[str, object]] = []
    subgroup_rows: list[dict[str, object]] = []

    for model_id, rows in binary_by_model.items():
        y_true = [int(r["y_true"]) for r in rows]
        scores = [float(r["y_score"]) for r in rows]
        model_summary_rows.append({
            "model_id": model_id,
            "n": len(rows),
            "positive_rate": round(sum(y_true) / len(y_true), 4),
            "roc_auc": round(roc_auc(y_true, scores), 4),
            "average_precision": round(average_precision(y_true, scores), 4),
            "brier_score": round(brier_score(y_true, scores), 4),
            "log_loss": round(log_loss(y_true, scores), 4),
        })

        for threshold_policy in [t for t in thresholds if t["model_id"] == model_id]:
            threshold = float(threshold_policy["threshold"])
            m = threshold_metrics(y_true, scores, threshold)
            threshold_rows.append({
                "model_id": model_id,
                "policy_id": threshold_policy["policy_id"],
                "threshold": threshold,
                "policy_name": threshold_policy["policy_name"],
                **{k: round(v, 4) if isinstance(v, float) else v for k, v in m.items()},
                "expected_error_cost": round(
                    m["fp"] * float(threshold_policy["false_positive_cost"])
                    + m["fn"] * float(threshold_policy["false_negative_cost"]),
                    4,
                ),
            })

        for cal in calibration_bins(y_true, scores, bins=5):
            calibration_rows.append({"model_id": model_id, **{k: round(v, 4) if isinstance(v, float) else v for k, v in cal.items()}})

        by_subgroup: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            by_subgroup[row["subgroup"]].append(row)
        for subgroup, subgroup_model_rows in by_subgroup.items():
            sy = [int(r["y_true"]) for r in subgroup_model_rows]
            ss = [float(r["y_score"]) for r in subgroup_model_rows]
            tm = threshold_metrics(sy, ss, 0.5)
            subgroup_rows.append({
                "model_id": model_id,
                "subgroup": subgroup,
                "n": len(subgroup_model_rows),
                "positive_rate": round(sum(sy) / len(sy), 4),
                "precision_at_0_5": round(tm["precision"], 4),
                "recall_at_0_5": round(tm["recall"], 4),
                "accuracy_at_0_5": round(tm["accuracy"], 4),
                "brier_score": round(brier_score(sy, ss), 4),
            })

    regression_by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in regression:
        regression_by_model[row["model_id"]].append(row)

    regression_rows: list[dict[str, object]] = []
    for model_id, rows in regression_by_model.items():
        y_true = [float(r["y_true"]) for r in rows]
        y_pred = [float(r["y_pred"]) for r in rows]
        m = regression_metrics(y_true, y_pred)
        regression_rows.append({"model_id": model_id, **{k: round(v, 4) for k, v in m.items()}})

    scorecard_rows: list[dict[str, object]] = []
    for row in scorecard:
        observed = float(row["observed_value"])
        limit = float(row["acceptable_limit"])
        metric_name = row["metric_name"]
        if metric_name in {"mae", "tail_error_p90", "brier_score"}:
            within_limit = observed <= limit
        else:
            within_limit = observed >= limit
        scorecard_rows.append({
            **row,
            "within_limit": within_limit,
            "gap_to_limit": round(observed - limit, 4),
        })

    monitoring_rows: list[dict[str, object]] = []
    for row in monitoring:
        drift = float(row["drift_index"])
        escalation = drift >= 0.18 or row["status"] == "escalate"
        monitoring_rows.append({
            **row,
            "drift_escalation_flag": escalation,
        })

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Model Evaluation and Performance Metrics",
        "workflow": "model-evaluation-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "model_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "binary_predictions": {"path": str(binary_path), "sha256": sha256_file(binary_path), "rows": len(binary)},
            "regression_predictions": {"path": str(regression_path), "sha256": sha256_file(regression_path), "rows": len(regression)},
            "threshold_policies": {"path": str(thresholds_path), "sha256": sha256_file(thresholds_path), "rows": len(thresholds)},
            "metric_scorecard": {"path": str(scorecard_path), "sha256": sha256_file(scorecard_path), "rows": len(scorecard)},
            "monitoring_windows": {"path": str(monitoring_path), "sha256": sha256_file(monitoring_path), "rows": len(monitoring)},
        },
        "outputs": {
            "model_summary": "outputs/model_evaluation_summary_python.csv",
            "threshold_metrics": "outputs/threshold_metrics_python.csv",
            "calibration_bins": "outputs/calibration_bins_python.csv",
            "subgroup_metrics": "outputs/subgroup_metrics_python.csv",
            "regression_metrics": "outputs/regression_metrics_python.csv",
            "scorecard_limits": "outputs/metric_scorecard_limits_python.csv",
            "monitoring_flags": "outputs/monitoring_flags_python.csv",
            "manifest": "outputs/model_evaluation_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "model_evaluation_summary_python.csv", model_summary_rows)
    write_csv(ROOT / "outputs" / "threshold_metrics_python.csv", threshold_rows)
    write_csv(ROOT / "outputs" / "calibration_bins_python.csv", calibration_rows)
    write_csv(ROOT / "outputs" / "subgroup_metrics_python.csv", subgroup_rows)
    write_csv(ROOT / "outputs" / "regression_metrics_python.csv", regression_rows)
    write_csv(ROOT / "outputs" / "metric_scorecard_limits_python.csv", scorecard_rows)
    write_csv(ROOT / "outputs" / "monitoring_flags_python.csv", monitoring_rows)
    (ROOT / "outputs" / "model_evaluation_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Model evaluation scorecard complete")
    print(json.dumps({
        "models": len(registry),
        "binary_predictions": len(binary),
        "regression_predictions": len(regression),
        "threshold_policies": len(thresholds),
        "monitoring_windows": len(monitoring),
    }, indent=2))


if __name__ == "__main__":
    main()
