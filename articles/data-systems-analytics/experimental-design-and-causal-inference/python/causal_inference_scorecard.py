#!/usr/bin/env python3
"""
Python Workflow: Causal Design and Inference Scorecard

This workflow estimates simple causal contrasts and creates design-readiness
records for randomized, observational, difference-in-differences, and
regression-discontinuity examples using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import statistics
import sys
import platform
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
        "warn": 0.55,
        "planned": 0.45,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.45}.get(value, 0.1)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def diff_in_means(rows: list[dict[str, str]]) -> dict[str, float]:
    treated = [float(r["outcome"]) for r in rows if r["treatment"] == "1"]
    control = [float(r["outcome"]) for r in rows if r["treatment"] == "0"]
    return {
        "treated_mean": mean(treated),
        "control_mean": mean(control),
        "difference_in_means": mean(treated) - mean(control),
        "treated_n": len(treated),
        "control_n": len(control),
    }

def ipw_ate(rows: list[dict[str, str]]) -> float:
    weighted_treated = []
    weighted_control = []
    for r in rows:
        y = float(r["outcome"])
        t = int(r["treatment"])
        p = min(max(float(r["propensity_score"]), 0.01), 0.99)
        if t == 1:
            weighted_treated.append(y / p)
        else:
            weighted_control.append(y / (1 - p))
    return mean(weighted_treated) - mean(weighted_control)

def did_estimate(rows: list[dict[str, str]]) -> dict[str, float]:
    treated_pre = [float(r["outcome"]) for r in rows if r["treatment_group"] == "1" and r["post"] == "0"]
    treated_post = [float(r["outcome"]) for r in rows if r["treatment_group"] == "1" and r["post"] == "1"]
    control_pre = [float(r["outcome"]) for r in rows if r["treatment_group"] == "0" and r["post"] == "0"]
    control_post = [float(r["outcome"]) for r in rows if r["treatment_group"] == "0" and r["post"] == "1"]
    return {
        "treated_change": mean(treated_post) - mean(treated_pre),
        "control_change": mean(control_post) - mean(control_pre),
        "difference_in_differences": (mean(treated_post) - mean(treated_pre)) - (mean(control_post) - mean(control_pre)),
    }

def rdd_local_difference(rows: list[dict[str, str]], bandwidth: float = 2.0) -> dict[str, float]:
    near = [r for r in rows if abs(float(r["running_variable"]) - float(r["cutoff"])) <= bandwidth]
    treated = [float(r["outcome"]) for r in near if r["treatment"] == "1"]
    control = [float(r["outcome"]) for r in near if r["treatment"] == "0"]
    return {
        "bandwidth": bandwidth,
        "treated_mean_near_cutoff": mean(treated),
        "control_mean_near_cutoff": mean(control),
        "local_cutoff_difference": mean(treated) - mean(control),
        "near_cutoff_n": len(near),
    }

def main() -> None:
    registry_path = ROOT / "data" / "causal_study_registry.csv"
    units_path = ROOT / "data" / "experiment_units.csv"
    did_path = ROOT / "data" / "did_panel.csv"
    rdd_path = ROOT / "data" / "rdd_units.csv"
    checks_path = ROOT / "data" / "assumption_checks.csv"
    factorial_path = ROOT / "data" / "factorial_design.csv"

    registry = read_csv(registry_path)
    units = read_csv(units_path)
    did = read_csv(did_path)
    rdd = read_csv(rdd_path)
    checks = read_csv(checks_path)
    factorial = read_csv(factorial_path)

    units_by_study = defaultdict(list)
    for row in units:
        units_by_study[row["study_id"]].append(row)

    checks_by_study = defaultdict(list)
    for row in checks:
        checks_by_study[row["study_id"]].append(row)

    effect_rows = []
    readiness_rows = []
    assumption_rows = []

    for study in registry:
        study_id = study["study_id"]
        design = study["design_type"]
        design_strength = {
            "randomized_experiment": 1.0,
            "regression_discontinuity": 0.82,
            "difference_in_differences": 0.78,
            "target_trial_emulation": 0.72,
            "observational_regression": 0.35,
        }.get(design, 0.5)

        evidence_score = 0.45
        if study_id in units_by_study:
            dim = diff_in_means(units_by_study[study_id])
            ipw = ipw_ate(units_by_study[study_id])
            effect_rows.append({
                "study_id": study_id,
                "design_type": design,
                "estimand": study["estimand"],
                **{k: round(v, 4) for k, v in dim.items()},
                "ipw_ate": round(ipw, 4),
            })
            evidence_score = 0.7

        if study_id == "study003":
            estimate = did_estimate(did)
            effect_rows.append({
                "study_id": study_id,
                "design_type": design,
                "estimand": study["estimand"],
                **{k: round(v, 4) for k, v in estimate.items()},
            })
            evidence_score = 0.7

        if study_id == "study002":
            estimate = rdd_local_difference(rdd, bandwidth=2.0)
            effect_rows.append({
                "study_id": study_id,
                "design_type": design,
                "estimand": study["estimand"],
                **{k: round(v, 4) for k, v in estimate.items()},
            })
            evidence_score = 0.65

        study_checks = checks_by_study[study_id]
        check_scores = []
        for check in study_checks:
            base = status_score(check["status"])
            score = max(0.0, base - (severity_penalty(check["severity"]) if check["status"] != "pass" else 0.0))
            check_scores.append(score)
            assumption_rows.append({
                "study_id": study_id,
                "assumption": check["assumption"],
                "status": check["status"],
                "severity": check["severity"],
                "assumption_score": round(score, 3),
                "remediation": check["remediation"],
            })
        assumption_score = mean(check_scores) if check_scores else 0.45

        readiness = round(
            0.28 * design_strength
            + 0.22 * evidence_score
            + 0.26 * assumption_score
            + 0.14 * status_score(study["status"])
            + 0.10 * (0.65 if study["risk_level"] == "high" else 0.85),
            3,
        )

        readiness_rows.append({
            "study_id": study_id,
            "study_name": study["study_name"],
            "design_type": design,
            "estimand": study["estimand"],
            "status": study["status"],
            "risk_level": study["risk_level"],
            "design_strength": round(design_strength, 3),
            "evidence_score": round(evidence_score, 3),
            "assumption_score": round(assumption_score, 3),
            "causal_readiness_score": readiness,
            "causal_readiness_gap": round(1.0 - readiness, 3),
        })

    factorial_rows = []
    for row in factorial:
        factorial_rows.append({
            "study_id": row["study_id"],
            "factor_a": row["factor_a"],
            "factor_b": row["factor_b"],
            "n": row["n"],
            "mean_outcome": row["mean_outcome"],
        })

    design_summary = [
        {"design_type": design, "study_count": count}
        for design, count in sorted(Counter(row["design_type"] for row in registry).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Experimental Design and Causal Inference",
        "workflow": "causal-design-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "causal_study_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "experiment_units": {"path": str(units_path), "sha256": sha256_file(units_path), "rows": len(units)},
            "did_panel": {"path": str(did_path), "sha256": sha256_file(did_path), "rows": len(did)},
            "rdd_units": {"path": str(rdd_path), "sha256": sha256_file(rdd_path), "rows": len(rdd)},
            "assumption_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
        },
    }

    write_csv(ROOT / "outputs" / "causal_readiness_scorecard_python.csv", readiness_rows)
    write_csv(ROOT / "outputs" / "causal_effect_estimates_python.csv", effect_rows)
    write_csv(ROOT / "outputs" / "assumption_review_python.csv", assumption_rows)
    write_csv(ROOT / "outputs" / "factorial_design_summary_python.csv", factorial_rows)
    write_csv(ROOT / "outputs" / "design_type_summary_python.csv", design_summary)
    (ROOT / "outputs" / "causal_inference_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Causal inference scorecard complete")
    print(json.dumps({"studies": len(registry), "assumption_checks": len(checks), "effect_rows": len(effect_rows)}, indent=2))

if __name__ == "__main__":
    main()
