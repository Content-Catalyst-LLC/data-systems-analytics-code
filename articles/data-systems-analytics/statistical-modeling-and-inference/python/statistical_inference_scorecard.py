#!/usr/bin/env python3
"""
Python Workflow: Statistical Modeling and Inference Scorecard

This workflow estimates sample summaries, confidence intervals, regression
coefficients, diagnostic-review scores, and inference-readiness records using
only the Python standard library.
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

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "in_review": 0.7,
        "watch": 0.55,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.45}.get(value, 0.1)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def sample_sd(values: list[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0

def ci_mean(values: list[float], z: float = 1.96) -> dict[str, float]:
    m = mean(values)
    sd = sample_sd(values)
    se = sd / math.sqrt(len(values)) if values else 0.0
    return {"mean": m, "standard_error": se, "ci_low": m - z * se, "ci_high": m + z * se, "n": len(values)}

def simple_linear_regression(x: list[float], y: list[float]) -> dict[str, float]:
    xbar = mean(x)
    ybar = mean(y)
    sxx = sum((xi - xbar) ** 2 for xi in x)
    sxy = sum((xi - xbar) * (yi - ybar) for xi, yi in zip(x, y))
    slope = sxy / sxx if sxx else 0.0
    intercept = ybar - slope * xbar
    fitted = [intercept + slope * xi for xi in x]
    residuals = [yi - fi for yi, fi in zip(y, fitted)]
    rss = sum(r ** 2 for r in residuals)
    sigma2 = rss / max(len(x) - 2, 1)
    slope_se = math.sqrt(sigma2 / sxx) if sxx else 0.0
    t_value = slope / slope_se if slope_se else 0.0
    return {
        "intercept": intercept,
        "slope": slope,
        "slope_standard_error": slope_se,
        "slope_ci_low": slope - 1.96 * slope_se,
        "slope_ci_high": slope + 1.96 * slope_se,
        "t_value": t_value,
        "rss": rss,
        "rmse": math.sqrt(rss / len(x)),
    }

def main() -> None:
    observations_path = ROOT / "data" / "sample_observations.csv"
    registry_path = ROOT / "data" / "model_registry.csv"
    claims_path = ROOT / "data" / "inference_claims.csv"
    checks_path = ROOT / "data" / "diagnostic_checks.csv"
    robustness_path = ROOT / "data" / "robustness_checks.csv"

    observations = read_csv(observations_path)
    registry = read_csv(registry_path)
    claims = read_csv(claims_path)
    checks = read_csv(checks_path)
    robustness = read_csv(robustness_path)

    values_by_group = defaultdict(list)
    for row in observations:
        values_by_group[row["group_id"]].append(float(row["outcome"]))

    group_rows = []
    for group, vals in sorted(values_by_group.items()):
        ci = ci_mean(vals)
        group_rows.append({
            "group_id": group,
            **{k: round(v, 4) if isinstance(v, float) else v for k, v in ci.items()},
        })

    group_a = values_by_group["A"]
    group_b = values_by_group["B"]
    diff = mean(group_b) - mean(group_a)
    se_diff = math.sqrt((sample_sd(group_a) ** 2 / len(group_a)) + (sample_sd(group_b) ** 2 / len(group_b)))
    difference_rows = [{
        "contrast": "B_minus_A",
        "mean_difference": round(diff, 4),
        "standard_error": round(se_diff, 4),
        "ci_low": round(diff - 1.96 * se_diff, 4),
        "ci_high": round(diff + 1.96 * se_diff, 4),
    }]

    x = [float(row["predictor_x"]) for row in observations]
    y = [float(row["outcome"]) for row in observations]
    reg = simple_linear_regression(x, y)
    regression_rows = [{k: round(v, 4) for k, v in reg.items()}]

    checks_by_model = defaultdict(list)
    for check in checks:
        checks_by_model[check["model_id"]].append(check)

    robustness_by_model = defaultdict(list)
    for row in robustness:
        robustness_by_model[row["model_id"]].append(row)

    readiness_rows = []
    diagnostic_rows = []
    for model in registry:
        model_id = model["model_id"]

        model_checks = checks_by_model[model_id]
        check_scores = []
        for check in model_checks:
            base = status_score(check["status"])
            score = max(0.0, base - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0))
            check_scores.append(score)
            diagnostic_rows.append({
                "model_id": model_id,
                "check_type": check["check_type"],
                "status": check["status"],
                "severity": check["severity"],
                "diagnostic_score": round(score, 3),
                "remediation": check["remediation"],
            })
        diagnostic_score = mean(check_scores) if check_scores else 0.45

        model_claims = [row for row in claims if row["model_id"] == model_id]
        claim_scores = []
        for claim in model_claims:
            effect = abs(float(claim["effect_size"]))
            threshold = abs(float(claim["practical_threshold"]))
            interval_crosses_zero = float(claim["confidence_low"]) <= 0 <= float(claim["confidence_high"])
            practical_score = 1.0 if effect >= threshold else 0.35
            uncertainty_score = 0.4 if interval_crosses_zero else 0.9
            p_value_score = 0.5 if claim["claim_type"] == "p_value_threshold" else 0.8
            claim_scores.append(0.35 * practical_score + 0.35 * uncertainty_score + 0.30 * p_value_score)
        claim_quality = mean(claim_scores) if claim_scores else 0.45

        model_robust = robustness_by_model[model_id]
        robustness_scores = [status_score(row["status"]) for row in model_robust]
        robustness_score = mean(robustness_scores) if robustness_scores else 0.45

        assumption_score = 0.2 if model["assumption_profile"] == "unclear_assumptions" else 0.75
        readiness = round(
            0.20 * status_score(model["status"])
            + 0.22 * diagnostic_score
            + 0.20 * claim_quality
            + 0.18 * robustness_score
            + 0.20 * assumption_score,
            3,
        )

        readiness_rows.append({
            "model_id": model_id,
            "model_family": model["model_family"],
            "estimand": model["estimand"],
            "status": model["status"],
            "risk_level": model["risk_level"],
            "diagnostic_score": round(diagnostic_score, 3),
            "claim_quality": round(claim_quality, 3),
            "robustness_score": round(robustness_score, 3),
            "assumption_score": round(assumption_score, 3),
            "inference_readiness_score": readiness,
            "inference_readiness_gap": round(1.0 - readiness, 3),
        })

    status_summary = [
        {"status": status, "count": count}
        for status, count in sorted(Counter(row["status"] for row in registry).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Statistical Modeling and Inference",
        "workflow": "statistical-inference-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "sample_observations": {"path": str(observations_path), "sha256": sha256_file(observations_path), "rows": len(observations)},
            "model_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "inference_claims": {"path": str(claims_path), "sha256": sha256_file(claims_path), "rows": len(claims)},
            "diagnostic_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "robustness_checks": {"path": str(robustness_path), "sha256": sha256_file(robustness_path), "rows": len(robustness)},
        },
    }

    write_csv(ROOT / "outputs" / "group_confidence_intervals_python.csv", group_rows)
    write_csv(ROOT / "outputs" / "mean_difference_python.csv", difference_rows)
    write_csv(ROOT / "outputs" / "simple_regression_python.csv", regression_rows)
    write_csv(ROOT / "outputs" / "diagnostic_review_python.csv", diagnostic_rows)
    write_csv(ROOT / "outputs" / "inference_readiness_scorecard_python.csv", readiness_rows)
    write_csv(ROOT / "outputs" / "model_status_summary_python.csv", status_summary)
    (ROOT / "outputs" / "statistical_inference_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Statistical inference scorecard complete")
    print(json.dumps({"observations": len(observations), "models": len(registry), "claims": len(claims)}, indent=2))

if __name__ == "__main__":
    main()
