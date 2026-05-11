#!/usr/bin/env python3
"""
Python Workflow: Visualization and Analytical Communication Integrity Scorecard

This workflow evaluates visualizations using chart fit, encoding quality,
uncertainty placement, annotation, accessibility, evidence traceability,
audience fit, review status, and output control.
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


def bool_value(value: str) -> bool:
    return value.strip().lower() == "true"


def status_score(value: str) -> float:
    return {"approved": 1.0, "in_review": 0.7, "needs_revision": 0.25, "weak": 0.2}.get(value, 0.5)


def fit_score(value: str) -> float:
    return {"high": 1.0, "medium": 0.7, "low": 0.25}.get(value, 0.5)


def perceptual_score(value: str) -> float:
    return {"high": 1.0, "medium": 0.7, "low": 0.25}.get(value, 0.5)


def accessibility_score(status: str, severity: str) -> float:
    base = {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(status, 0.5)
    if severity == "high" and status != "pass":
        return min(base, 0.5)
    return base


def traceability_score(value: str) -> float:
    return {"complete": 1.0, "partial": 0.5, "missing": 0.0}.get(value, 0.4)


def main() -> None:
    inventory_path = ROOT / "data" / "visualization_inventory.csv"
    chart_path = ROOT / "data" / "chart_assessments.csv"
    encoding_path = ROOT / "data" / "encoding_assessments.csv"
    uncertainty_path = ROOT / "data" / "uncertainty_elements.csv"
    annotation_path = ROOT / "data" / "annotation_elements.csv"
    accessibility_path = ROOT / "data" / "accessibility_checks.csv"
    evidence_path = ROOT / "data" / "evidence_links.csv"
    audience_path = ROOT / "data" / "audience_contexts.csv"
    review_path = ROOT / "data" / "review_checkpoints.csv"
    output_path = ROOT / "data" / "visual_outputs.csv"

    visuals = read_csv(inventory_path)
    charts = read_csv(chart_path)
    encodings = read_csv(encoding_path)
    uncertainties = read_csv(uncertainty_path)
    annotations = read_csv(annotation_path)
    accessibility = read_csv(accessibility_path)
    evidence = read_csv(evidence_path)
    audiences = read_csv(audience_path)
    reviews = read_csv(review_path)
    outputs = read_csv(output_path)

    charts_by_visual = defaultdict(list)
    for row in charts:
        charts_by_visual[row["visual_id"]].append(row)

    encodings_by_visual = defaultdict(list)
    for row in encodings:
        encodings_by_visual[row["visual_id"]].append(row)

    uncertainty_by_visual = defaultdict(list)
    for row in uncertainties:
        uncertainty_by_visual[row["visual_id"]].append(row)

    annotations_by_visual = defaultdict(list)
    for row in annotations:
        annotations_by_visual[row["visual_id"]].append(row)

    accessibility_by_visual = defaultdict(list)
    for row in accessibility:
        accessibility_by_visual[row["visual_id"]].append(row)

    evidence_by_visual = defaultdict(list)
    for row in evidence:
        evidence_by_visual[row["visual_id"]].append(row)

    audience_by_visual = defaultdict(list)
    for row in audiences:
        audience_by_visual[row["visual_id"]].append(row)

    reviews_by_visual = defaultdict(list)
    for row in reviews:
        reviews_by_visual[row["visual_id"]].append(row)

    outputs_by_visual = defaultdict(list)
    for row in outputs:
        outputs_by_visual[row["visual_id"]].append(row)

    rows = []
    for visual in visuals:
        visual_id = visual["visual_id"]

        visual_charts = charts_by_visual[visual_id]
        chart_fit = sum(fit_score(c["chart_fit"]) for c in visual_charts) / len(visual_charts) if visual_charts else 0.5

        visual_encodings = encodings_by_visual[visual_id]
        encoding_scores = []
        for encoding in visual_encodings:
            flags = [
                bool_value(encoding["axis_baseline_appropriate"]),
                bool_value(encoding["sorting_appropriate"]),
                not bool_value(encoding["color_dependency"]),
            ]
            encoding_scores.append(
                0.45 * perceptual_score(encoding["perceptual_accuracy"])
                + 0.25 * status_score(encoding["label_quality"])
                + 0.30 * (sum(flags) / len(flags))
            )
        encoding_quality = sum(encoding_scores) / len(encoding_scores) if encoding_scores else 0.5

        visual_uncertainty = uncertainty_by_visual[visual_id]
        uncertainty_scores = []
        for row in visual_uncertainty:
            near_claim = 1.0 if bool_value(row["near_claim"]) else 0.3
            materiality_penalty = 0.2 if row["materiality"] == "high" and not bool_value(row["near_claim"]) else 0.0
            uncertainty_scores.append(max(0.0, near_claim * status_score(row["statement_quality"]) - materiality_penalty))
        uncertainty_score = sum(uncertainty_scores) / len(uncertainty_scores) if uncertainty_scores else 0.6

        visual_annotations = annotations_by_visual[visual_id]
        annotation_scores = []
        for row in visual_annotations:
            emphasis = {"low": 1.0, "medium": 0.75, "high": 0.25}.get(row["emphasis_risk"], 0.5)
            annotation_scores.append(
                status_score(row["text_quality"])
                * (1.0 if bool_value(row["evidence_linked"]) else 0.4)
                * (1.0 if bool_value(row["near_relevant_visual"]) else 0.5)
                * emphasis
            )
        annotation_quality = sum(annotation_scores) / len(annotation_scores) if annotation_scores else 0.6

        visual_accessibility = accessibility_by_visual[visual_id]
        accessibility_value = (
            sum(accessibility_score(a["status"], a["severity"]) for a in visual_accessibility) / len(visual_accessibility)
            if visual_accessibility else 0.6
        )

        visual_evidence = evidence_by_visual[visual_id]
        evidence_traceability = (
            sum(traceability_score(e["traceability_status"]) * status_score(e["review_status"]) for e in visual_evidence) / len(visual_evidence)
            if visual_evidence else 0.5
        )

        visual_audience = audience_by_visual[visual_id]
        audience_scores = []
        for row in visual_audience:
            audience_scores.append(
                0.40 * bool_value(row["summary_required"])
                + 0.30 * bool_value(row["method_reference_required"])
                + 0.30 * bool_value(row["decision_record_required"])
            )
        audience_fit = sum(audience_scores) / len(audience_scores) if audience_scores else 0.6

        visual_reviews = reviews_by_visual[visual_id]
        review_scores = []
        for row in visual_reviews:
            blocking_penalty = min(int(row["blocking_issues"]) * 0.2, 0.6)
            review_scores.append(max(0.0, status_score(row["status"]) - blocking_penalty))
        review_score_value = sum(review_scores) / len(review_scores) if visual_reviews else 0.4

        visual_outputs = outputs_by_visual[visual_id]
        output_scores = []
        for row in visual_outputs:
            output_scores.append(
                0.35 * bool_value(row["versioned"])
                + 0.35 * bool_value(row["archived"])
                + 0.30 * bool_value(row["hash_recorded"])
            )
        output_control = sum(output_scores) / len(output_scores) if visual_outputs else 0.0

        visual_integrity_score = round(
            0.16 * chart_fit
            + 0.16 * encoding_quality
            + 0.13 * uncertainty_score
            + 0.12 * annotation_quality
            + 0.12 * accessibility_value
            + 0.11 * evidence_traceability
            + 0.08 * audience_fit
            + 0.07 * review_score_value
            + 0.05 * output_control,
            3,
        )

        rows.append({
            "visual_id": visual_id,
            "visual_title": visual["visual_title"],
            "visualization_context": visual["visualization_context"],
            "status": visual["status"],
            "chart_fit": round(chart_fit, 3),
            "encoding_quality": round(encoding_quality, 3),
            "uncertainty_score": round(uncertainty_score, 3),
            "annotation_quality": round(annotation_quality, 3),
            "accessibility_score": round(accessibility_value, 3),
            "evidence_traceability": round(evidence_traceability, 3),
            "audience_fit": round(audience_fit, 3),
            "review_score": round(review_score_value, 3),
            "output_control": round(output_control, 3),
            "visual_integrity_score": visual_integrity_score,
            "visual_integrity_gap": round(1.0 - visual_integrity_score, 3),
        })

    chart_type_rows = [
        {"chart_type": chart_type, "chart_count": count}
        for chart_type, count in sorted(Counter(c["chart_type"] for c in charts).items())
    ]

    status_rows = [
        {"status": status, "visual_count": count}
        for status, count in sorted(Counter(v["status"] for v in visuals).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Visualization and Analytical Communication",
        "workflow": "visualization-integrity-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "visualization_inventory": {"path": str(inventory_path), "sha256": sha256_file(inventory_path), "rows": len(visuals)},
            "chart_assessments": {"path": str(chart_path), "sha256": sha256_file(chart_path), "rows": len(charts)},
            "encoding_assessments": {"path": str(encoding_path), "sha256": sha256_file(encoding_path), "rows": len(encodings)},
            "uncertainty_elements": {"path": str(uncertainty_path), "sha256": sha256_file(uncertainty_path), "rows": len(uncertainties)},
            "annotation_elements": {"path": str(annotation_path), "sha256": sha256_file(annotation_path), "rows": len(annotations)},
            "accessibility_checks": {"path": str(accessibility_path), "sha256": sha256_file(accessibility_path), "rows": len(accessibility)},
            "evidence_links": {"path": str(evidence_path), "sha256": sha256_file(evidence_path), "rows": len(evidence)},
            "audience_contexts": {"path": str(audience_path), "sha256": sha256_file(audience_path), "rows": len(audiences)},
            "review_checkpoints": {"path": str(review_path), "sha256": sha256_file(review_path), "rows": len(reviews)},
            "visual_outputs": {"path": str(output_path), "sha256": sha256_file(output_path), "rows": len(outputs)},
        },
        "outputs": {
            "scorecard": "outputs/visualization_integrity_scorecard_python.csv",
            "chart_type_summary": "outputs/chart_type_summary_python.csv",
            "status_summary": "outputs/visual_status_summary_python.csv",
            "manifest": "outputs/visualization_integrity_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "visualization_integrity_scorecard_python.csv", rows)
    write_csv(ROOT / "outputs" / "chart_type_summary_python.csv", chart_type_rows)
    write_csv(ROOT / "outputs" / "visual_status_summary_python.csv", status_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "visualization_integrity_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Visualization and analytical communication integrity scorecard complete")
    print(json.dumps({
        "visuals": len(visuals),
        "charts": len(charts),
        "encodings": len(encodings),
        "uncertainty_elements": len(uncertainties),
        "annotations": len(annotations),
    }, indent=2))


if __name__ == "__main__":
    main()
