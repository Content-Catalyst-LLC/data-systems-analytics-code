#!/usr/bin/env python3
"""
Python Workflow: Dashboard and Data Storytelling Integrity Scorecard

This workflow evaluates dashboard and story quality using KPI context,
view focus, filter burden, linked-view design, story sequence, annotation
quality, accessibility checks, governance review, and evidence traceability.
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


def design_risk_score(value: str) -> float:
    return {"low": 1.0, "medium": 0.7, "high": 0.25}.get(value, 0.5)


def complexity_penalty(value: str) -> float:
    return {"low": 0.0, "medium": 0.08, "high": 0.18}.get(value, 0.1)


def accessibility_score(status: str, severity: str) -> float:
    base = {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(status, 0.5)
    if severity == "high" and status != "pass":
        return min(base, 0.5)
    return base


def traceability_score(value: str) -> float:
    return {"complete": 1.0, "partial": 0.5, "missing": 0.0}.get(value, 0.4)


def main() -> None:
    inventory_path = ROOT / "data" / "dashboard_inventory.csv"
    kpi_path = ROOT / "data" / "kpi_definitions.csv"
    filter_path = ROOT / "data" / "filter_controls.csv"
    views_path = ROOT / "data" / "linked_views.csv"
    story_path = ROOT / "data" / "story_points.csv"
    annotation_path = ROOT / "data" / "annotations.csv"
    interaction_path = ROOT / "data" / "interaction_events.csv"
    accessibility_path = ROOT / "data" / "accessibility_checks.csv"
    governance_path = ROOT / "data" / "governance_checks.csv"
    evidence_path = ROOT / "data" / "evidence_links.csv"

    dashboards = read_csv(inventory_path)
    kpis = read_csv(kpi_path)
    filters = read_csv(filter_path)
    views = read_csv(views_path)
    stories = read_csv(story_path)
    annotations = read_csv(annotation_path)
    interactions = read_csv(interaction_path)
    accessibility = read_csv(accessibility_path)
    governance = read_csv(governance_path)
    evidence = read_csv(evidence_path)

    kpis_by_dashboard = defaultdict(list)
    for row in kpis:
        kpis_by_dashboard[row["dashboard_id"]].append(row)

    filters_by_dashboard = defaultdict(list)
    for row in filters:
        filters_by_dashboard[row["dashboard_id"]].append(row)

    views_by_dashboard = defaultdict(list)
    for row in views:
        views_by_dashboard[row["dashboard_id"]].append(row)

    stories_by_dashboard = defaultdict(list)
    for row in stories:
        stories_by_dashboard[row["dashboard_id"]].append(row)

    annotations_by_dashboard = defaultdict(list)
    for row in annotations:
        annotations_by_dashboard[row["dashboard_id"]].append(row)

    interactions_by_dashboard = defaultdict(list)
    for row in interactions:
        interactions_by_dashboard[row["dashboard_id"]].append(row)

    accessibility_by_dashboard = defaultdict(list)
    for row in accessibility:
        accessibility_by_dashboard[row["dashboard_id"]].append(row)

    governance_by_dashboard = defaultdict(list)
    for row in governance:
        governance_by_dashboard[row["dashboard_id"]].append(row)

    evidence_by_dashboard = defaultdict(list)
    for row in evidence:
        evidence_by_dashboard[row["dashboard_id"]].append(row)

    rows = []
    for dashboard in dashboards:
        dashboard_id = dashboard["dashboard_id"]

        dashboard_kpis = kpis_by_dashboard[dashboard_id]
        kpi_scores = []
        for kpi in dashboard_kpis:
            context_flags = [
                bool_value(kpi["baseline_present"]),
                bool_value(kpi["target_present"]),
                bool_value(kpi["trend_present"]),
                bool_value(kpi["denominator_present"]),
            ]
            kpi_scores.append((sum(context_flags) / len(context_flags)) * status_score(kpi["definition_status"]))
        kpi_context = sum(kpi_scores) / len(kpi_scores) if kpi_scores else 0.5

        view_count = int(dashboard["view_count"])
        filter_count = int(dashboard["filter_count"])
        view_focus = 1.0 if view_count <= 3 else max(0.25, 1.0 - 0.12 * (view_count - 3))

        dashboard_filters = filters_by_dashboard[dashboard_id]
        filter_scores = []
        for control in dashboard_filters:
            flags = [
                bool_value(control["default_state_visible"]),
                bool_value(control["reset_available"]),
                bool_value(control["consumer_relevant"]),
            ]
            filter_scores.append(max(0.0, sum(flags) / len(flags) - complexity_penalty(control["complexity_level"])))
        interaction_clarity = sum(filter_scores) / len(filter_scores) if filter_scores else 0.8
        interaction_burden = max(0.0, min(1.0, 1.0 - ((filter_count - 3) * 0.08 if filter_count > 3 else 0.0)))

        dashboard_views = views_by_dashboard[dashboard_id]
        linked_view_scores = []
        for view in dashboard_views:
            progressive = 1.0 if bool_value(view["progressive_disclosure"]) else 0.75
            linked_view_scores.append(progressive * design_risk_score(view["design_risk"]) * status_score(view["caption_quality"]))
        linked_view_quality = sum(linked_view_scores) / len(linked_view_scores) if linked_view_scores else 0.7

        dashboard_story_points = stories_by_dashboard[dashboard_id]
        story_scores = []
        for point in dashboard_story_points:
            uncertainty_visible = 1.0 if bool_value(point["uncertainty_visible"]) else 0.4
            story_scores.append(0.55 + 0.25 * uncertainty_visible + 0.20 * bool(point["linked_view_id"]))
        story_coherence = sum(story_scores) / len(story_scores) if story_scores else (0.8 if dashboard["dashboard_type"] != "guided_story" else 0.4)

        dashboard_annotations = annotations_by_dashboard[dashboard_id]
        annotation_scores = []
        for row in dashboard_annotations:
            annotation_scores.append(
                status_score(row["text_quality"])
                * (1.0 if bool_value(row["evidence_linked"]) else 0.4)
                * (1.0 if bool_value(row["near_relevant_visual"]) else 0.5)
                * design_risk_score(row["emphasis_risk"])
            )
        annotation_quality = sum(annotation_scores) / len(annotation_scores) if annotation_scores else 0.6

        dashboard_accessibility = accessibility_by_dashboard[dashboard_id]
        accessibility_value = (
            sum(accessibility_score(a["status"], a["severity"]) for a in dashboard_accessibility) / len(dashboard_accessibility)
            if dashboard_accessibility else 0.6
        )

        dashboard_governance = governance_by_dashboard[dashboard_id]
        governance_scores = []
        for row in dashboard_governance:
            blocking_penalty = 0.25 if bool_value(row["blocking_issue"]) else 0.0
            governance_scores.append(max(0.0, status_score(row["status"]) - blocking_penalty))
        governance_value = sum(governance_scores) / len(governance_scores) if governance_scores else 0.5

        dashboard_evidence = evidence_by_dashboard[dashboard_id]
        evidence_traceability = (
            sum(traceability_score(e["traceability_status"]) * status_score(e["review_status"]) for e in dashboard_evidence) / len(dashboard_evidence)
            if dashboard_evidence else 0.5
        )

        dash_integrity_score = round(
            0.14 * kpi_context
            + 0.12 * view_focus
            + 0.12 * interaction_clarity
            + 0.10 * interaction_burden
            + 0.12 * linked_view_quality
            + 0.10 * story_coherence
            + 0.10 * annotation_quality
            + 0.08 * accessibility_value
            + 0.07 * governance_value
            + 0.05 * evidence_traceability,
            3,
        )

        rows.append({
            "dashboard_id": dashboard_id,
            "dashboard_title": dashboard["dashboard_title"],
            "dashboard_type": dashboard["dashboard_type"],
            "status": dashboard["status"],
            "view_count": view_count,
            "filter_count": filter_count,
            "kpi_context": round(kpi_context, 3),
            "view_focus": round(view_focus, 3),
            "interaction_clarity": round(interaction_clarity, 3),
            "interaction_burden_score": round(interaction_burden, 3),
            "linked_view_quality": round(linked_view_quality, 3),
            "story_coherence": round(story_coherence, 3),
            "annotation_quality": round(annotation_quality, 3),
            "accessibility_score": round(accessibility_value, 3),
            "governance_score": round(governance_value, 3),
            "evidence_traceability": round(evidence_traceability, 3),
            "dashboard_integrity_score": dash_integrity_score,
            "dashboard_integrity_gap": round(1.0 - dash_integrity_score, 3),
        })

    type_rows = [
        {"dashboard_type": dashboard_type, "dashboard_count": count}
        for dashboard_type, count in sorted(Counter(d["dashboard_type"] for d in dashboards).items())
    ]

    status_rows = [
        {"status": status, "dashboard_count": count}
        for status, count in sorted(Counter(d["status"] for d in dashboards).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Interactive Dashboards and Data Storytelling",
        "workflow": "dashboard-storytelling-integrity-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "dashboard_inventory": {"path": str(inventory_path), "sha256": sha256_file(inventory_path), "rows": len(dashboards)},
            "kpi_definitions": {"path": str(kpi_path), "sha256": sha256_file(kpi_path), "rows": len(kpis)},
            "filter_controls": {"path": str(filter_path), "sha256": sha256_file(filter_path), "rows": len(filters)},
            "linked_views": {"path": str(views_path), "sha256": sha256_file(views_path), "rows": len(views)},
            "story_points": {"path": str(story_path), "sha256": sha256_file(story_path), "rows": len(stories)},
            "annotations": {"path": str(annotation_path), "sha256": sha256_file(annotation_path), "rows": len(annotations)},
            "interaction_events": {"path": str(interaction_path), "sha256": sha256_file(interaction_path), "rows": len(interactions)},
            "accessibility_checks": {"path": str(accessibility_path), "sha256": sha256_file(accessibility_path), "rows": len(accessibility)},
            "governance_checks": {"path": str(governance_path), "sha256": sha256_file(governance_path), "rows": len(governance)},
            "evidence_links": {"path": str(evidence_path), "sha256": sha256_file(evidence_path), "rows": len(evidence)},
        },
        "outputs": {
            "scorecard": "outputs/dashboard_storytelling_integrity_scorecard_python.csv",
            "type_summary": "outputs/dashboard_type_summary_python.csv",
            "status_summary": "outputs/dashboard_status_summary_python.csv",
            "manifest": "outputs/dashboard_storytelling_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "dashboard_storytelling_integrity_scorecard_python.csv", rows)
    write_csv(ROOT / "outputs" / "dashboard_type_summary_python.csv", type_rows)
    write_csv(ROOT / "outputs" / "dashboard_status_summary_python.csv", status_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "dashboard_storytelling_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Dashboard and data storytelling integrity scorecard complete")
    print(json.dumps({
        "dashboards": len(dashboards),
        "kpis": len(kpis),
        "filters": len(filters),
        "views": len(views),
        "story_points": len(stories),
    }, indent=2))


if __name__ == "__main__":
    main()
