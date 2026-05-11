#!/usr/bin/env python3
"""
Python Workflow: Descriptive Analytics and EDA Scorecard

This workflow produces profile summaries, missingness checks, distribution
statistics, subgroup comparisons, correlation estimates, outlier flags, and an
exploration-readiness score using only the Python standard library.
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

def parse_float(value: str) -> float | None:
    if value in {"", "NA", "NaN", "null", "None"}:
        return None
    try:
        return float(value)
    except ValueError:
        return None

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def quantile(values: list[float], q: float) -> float:
    vals = sorted(values)
    if not vals:
        return 0.0
    pos = (len(vals) - 1) * q
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return vals[int(pos)]
    return vals[lower] * (upper - pos) + vals[upper] * (pos - lower)

def status_score(value: str) -> float:
    return {"pass": 1.0, "in_review": 0.7, "warn": 0.45, "fail": 0.0}.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.40}.get(value, 0.1)

def correlation(x: list[float], y: list[float]) -> float:
    if len(x) < 2 or len(y) < 2:
        return 0.0
    mx = mean(x)
    my = mean(y)
    numerator = sum((a - mx) * (b - my) for a, b in zip(x, y))
    denominator = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return numerator / denominator if denominator else 0.0

def main() -> None:
    data_path = ROOT / "data" / "exploration_dataset.csv"
    profile_path = ROOT / "data" / "variable_profile.csv"
    checks_path = ROOT / "data" / "exploration_checks.csv"
    questions_path = ROOT / "data" / "exploration_questions.csv"

    records = read_csv(data_path)
    profile = read_csv(profile_path)
    checks = read_csv(checks_path)
    questions = read_csv(questions_path)

    numeric_vars = ["value", "volume", "quality_score", "response_time"]
    categorical_vars = ["segment", "region", "category", "period"]

    profile_rows = []
    for var in numeric_vars:
        values = [parse_float(row[var]) for row in records]
        present = [v for v in values if v is not None]
        missing = len(values) - len(present)
        q1 = quantile(present, 0.25)
        q3 = quantile(present, 0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = [v for v in present if v < lower or v > upper]
        profile_rows.append({
            "variable_name": var,
            "n": len(values),
            "non_missing": len(present),
            "missing": missing,
            "missing_rate": round(missing / len(values), 4),
            "mean": round(mean(present), 4),
            "median": round(quantile(present, 0.50), 4),
            "sd": round(statistics.stdev(present), 4) if len(present) > 1 else 0.0,
            "min": round(min(present), 4),
            "q1": round(q1, 4),
            "q3": round(q3, 4),
            "max": round(max(present), 4),
            "outlier_count_iqr": len(outliers),
        })

    categorical_rows = []
    for var in categorical_vars:
        counts = Counter(row[var] for row in records)
        for level, count in sorted(counts.items()):
            categorical_rows.append({
                "variable_name": var,
                "level": level,
                "count": count,
                "share": round(count / len(records), 4),
            })

    subgroup_rows = []
    by_segment_region = defaultdict(list)
    for row in records:
        value = parse_float(row["value"])
        if value is not None:
            by_segment_region[(row["segment"], row["region"])].append(value)
    for (segment, region), values in sorted(by_segment_region.items()):
        subgroup_rows.append({
            "segment": segment,
            "region": region,
            "n": len(values),
            "mean_value": round(mean(values), 4),
            "median_value": round(quantile(values, 0.5), 4),
            "min_value": round(min(values), 4),
            "max_value": round(max(values), 4),
        })

    missing_rows = []
    by_segment_region_all = defaultdict(lambda: {"n": 0, "missing": 0})
    for row in records:
        key = (row["segment"], row["region"])
        by_segment_region_all[key]["n"] += 1
        if parse_float(row["value"]) is None:
            by_segment_region_all[key]["missing"] += 1
    for (segment, region), vals in sorted(by_segment_region_all.items()):
        missing_rows.append({
            "segment": segment,
            "region": region,
            "n": vals["n"],
            "missing_value_count": vals["missing"],
            "missing_value_rate": round(vals["missing"] / vals["n"], 4),
        })

    pairs = [("value", "volume"), ("value", "quality_score"), ("value", "response_time"), ("volume", "quality_score")]
    bivariate_rows = []
    for left, right in pairs:
        xs = []
        ys = []
        for row in records:
            lx = parse_float(row[left])
            ry = parse_float(row[right])
            if lx is not None and ry is not None:
                xs.append(lx)
                ys.append(ry)
        bivariate_rows.append({
            "left_variable": left,
            "right_variable": right,
            "n_pairs": len(xs),
            "correlation": round(correlation(xs, ys), 4),
        })

    overall_values = [parse_float(row["value"]) for row in records]
    overall_values = [v for v in overall_values if v is not None]
    aggregate_risk_rows = [{
        "metric": "value",
        "overall_mean": round(mean(overall_values), 4),
        "overall_median": round(quantile(overall_values, 0.5), 4),
        "mean_minus_median": round(mean(overall_values) - quantile(overall_values, 0.5), 4),
        "interpretation": "Large mean-median gap indicates skew or outlier influence."
    }]

    check_rows = []
    check_scores = []
    for check in checks:
        score = max(0.0, status_score(check["status"]) - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0))
        check_scores.append(score)
        check_rows.append({
            "check_id": check["check_id"],
            "check_type": check["check_type"],
            "status": check["status"],
            "severity": check["severity"],
            "score": round(score, 3),
            "remediation": check["remediation"],
        })

    active_questions = sum(1 for q in questions if q["status"] == "active")
    readiness = round(
        0.25 * (1.0 if len(records) > 0 else 0.0)
        + 0.25 * mean(check_scores)
        + 0.15 * (1.0 if active_questions >= 3 else 0.6)
        + 0.15 * (1.0 if subgroup_rows else 0.0)
        + 0.10 * (1.0 if bivariate_rows else 0.0)
        + 0.10 * (1.0 if profile_rows else 0.0),
        3,
    )

    readiness_rows = [{
        "dataset": "exploration_dataset.csv",
        "records": len(records),
        "variables_profiled": len(profile),
        "numeric_variables_profiled": len(profile_rows),
        "categorical_levels_profiled": len(categorical_rows),
        "active_questions": active_questions,
        "exploration_readiness_score": readiness,
        "exploration_readiness_gap": round(1.0 - readiness, 3),
    }]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Descriptive Analytics and Data Exploration",
        "workflow": "descriptive-eda-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "exploration_dataset": {"path": str(data_path), "sha256": sha256_file(data_path), "rows": len(records)},
            "variable_profile": {"path": str(profile_path), "sha256": sha256_file(profile_path), "rows": len(profile)},
            "exploration_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "exploration_questions": {"path": str(questions_path), "sha256": sha256_file(questions_path), "rows": len(questions)},
        },
    }

    write_csv(ROOT / "outputs" / "numeric_profile_python.csv", profile_rows)
    write_csv(ROOT / "outputs" / "categorical_profile_python.csv", categorical_rows)
    write_csv(ROOT / "outputs" / "subgroup_summary_python.csv", subgroup_rows)
    write_csv(ROOT / "outputs" / "missingness_by_subgroup_python.csv", missing_rows)
    write_csv(ROOT / "outputs" / "bivariate_relationships_python.csv", bivariate_rows)
    write_csv(ROOT / "outputs" / "aggregation_risk_python.csv", aggregate_risk_rows)
    write_csv(ROOT / "outputs" / "exploration_check_scorecard_python.csv", check_rows)
    write_csv(ROOT / "outputs" / "exploration_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "descriptive_eda_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Descriptive analytics and EDA scorecard complete")
    print(json.dumps({"records": len(records), "numeric_variables": len(profile_rows), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
