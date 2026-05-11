#!/usr/bin/env python3
"""
Python Workflow: MDM and Entity Resolution Scorecard

This workflow evaluates match candidates, crosswalks, survivorship rules,
hierarchy edges, stewardship queues, external identifiers, privacy risk,
and provenance records as a connected master-data governance system.
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


def action_risk(action: str) -> float:
    return {
        "merge": 0.15,
        "link": 0.30,
        "steward_review": 0.45,
        "possible_link": 0.65,
        "block": 0.90,
    }.get(action, 0.50)


def review_score(status: str) -> float:
    return {"resolved": 1.0, "in_review": 0.6, "open": 0.2}.get(status, 0.3)


def risk_weight(value: str) -> float:
    return {"low": 0.25, "medium": 0.60, "high": 1.0}.get(value, 0.5)


def main() -> None:
    source_path = ROOT / "data" / "source_records.csv"
    candidates_path = ROOT / "data" / "candidate_matches.csv"
    masters_path = ROOT / "data" / "master_entities.csv"
    crosswalk_path = ROOT / "data" / "entity_crosswalk.csv"
    survivorship_path = ROOT / "data" / "survivorship_rules.csv"
    hierarchy_path = ROOT / "data" / "hierarchy_edges.csv"
    stewardship_path = ROOT / "data" / "stewardship_queue.csv"
    external_path = ROOT / "data" / "external_identifiers.csv"
    privacy_path = ROOT / "data" / "privacy_identity_risk.csv"
    lineage_path = ROOT / "data" / "mdm_lineage_events.csv"

    source_records = read_csv(source_path)
    candidates = read_csv(candidates_path)
    masters = read_csv(masters_path)
    crosswalk = read_csv(crosswalk_path)
    survivorship = read_csv(survivorship_path)
    hierarchy = read_csv(hierarchy_path)
    stewardship = read_csv(stewardship_path)
    external_ids = read_csv(external_path)
    privacy_risk = read_csv(privacy_path)
    lineage = read_csv(lineage_path)

    candidate_rows = []
    for row in candidates:
        score = float(row["match_score"])
        recommended = row["recommended_action"]
        review_required = bool_value(row["review_required"])
        merge_risk = round((1.0 - score) * 0.55 + action_risk(recommended) * 0.30 + (0.15 if review_required else 0.0), 3)

        candidate_rows.append({
            "candidate_id": row["candidate_id"],
            "left_record_id": row["left_record_id"],
            "right_record_id": row["right_record_id"],
            "entity_type": row["entity_type"],
            "match_method": row["match_method"],
            "match_score": score,
            "recommended_action": recommended,
            "review_required": review_required,
            "merge_risk_score": merge_risk,
        })

    crosswalk_by_master = defaultdict(list)
    for row in crosswalk:
        crosswalk_by_master[row["master_entity_id"]].append(row)

    hierarchy_by_child = Counter(row["child_entity_id"] for row in hierarchy)
    lineage_by_master = Counter(row["output_master_entity_id"] for row in lineage)
    external_by_master = defaultdict(list)
    for row in external_ids:
        external_by_master[row["master_entity_id"]].append(row)

    stewardship_by_master = defaultdict(list)
    for row in stewardship:
        if row["master_entity_id"]:
            stewardship_by_master[row["master_entity_id"]].append(row)

    privacy_by_master = {row["master_entity_id"]: row for row in privacy_risk}

    master_rows = []
    for master in masters:
        master_id = master["master_entity_id"]
        links = crosswalk_by_master.get(master_id, [])
        confidences = [float(link["confidence"]) for link in links]
        average_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        review_items = stewardship_by_master.get(master_id, [])
        review_maturity = sum(review_score(item["status"]) for item in review_items) / len(review_items) if review_items else 1.0

        external_verified = sum(item["verification_status"] == "verified" for item in external_by_master.get(master_id, []))
        external_total = len(external_by_master.get(master_id, []))
        external_score = 1.0 if external_total == 0 else external_verified / external_total

        lineage_score = 1.0 if lineage_by_master[master_id] else 0.0
        hierarchy_score = 1.0 if hierarchy_by_child[master_id] else 0.7

        privacy = privacy_by_master.get(master_id)
        privacy_penalty = 0.0
        if privacy:
            privacy_penalty = 0.15 * risk_weight(privacy["reidentification_risk"]) + 0.15 * risk_weight(privacy["linkage_sensitivity"])
            if privacy["purpose_review_status"] != "approved":
                privacy_penalty += 0.10

        identity_governance_score = round(
            max(
                0.0,
                0.30 * average_confidence
                + 0.20 * review_maturity
                + 0.15 * external_score
                + 0.15 * lineage_score
                + 0.10 * hierarchy_score
                + 0.10 * min(len(links) / 3.0, 1.0)
                - privacy_penalty,
            ),
            3,
        )

        master_rows.append({
            "master_entity_id": master_id,
            "master_name": master["master_name"],
            "entity_type": master["entity_type"],
            "domain": master["domain"],
            "authoritative_view": master["authoritative_view"],
            "linked_record_count": len(links),
            "average_link_confidence": round(average_confidence, 3),
            "review_maturity_score": round(review_maturity, 3),
            "external_identifier_score": round(external_score, 3),
            "lineage_score": lineage_score,
            "hierarchy_score": hierarchy_score,
            "identity_governance_score": identity_governance_score,
        })

    source_summary = [
        {"source_system": source, "record_count": count}
        for source, count in sorted(Counter(r["source_system"] for r in source_records).items())
    ]

    entity_type_summary = [
        {"entity_type": entity_type, "source_record_count": count}
        for entity_type, count in sorted(Counter(r["entity_type"] for r in source_records).items())
    ]

    survivorship_summary = [
        {"review_required": review_required, "rule_count": count}
        for review_required, count in sorted(Counter(r["review_required"] for r in survivorship).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Master Data Management and Entity Resolution",
        "workflow": "mdm-entity-resolution-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "source_records": {"path": str(source_path), "sha256": sha256_file(source_path), "rows": len(source_records)},
            "candidate_matches": {"path": str(candidates_path), "sha256": sha256_file(candidates_path), "rows": len(candidates)},
            "master_entities": {"path": str(masters_path), "sha256": sha256_file(masters_path), "rows": len(masters)},
            "entity_crosswalk": {"path": str(crosswalk_path), "sha256": sha256_file(crosswalk_path), "rows": len(crosswalk)},
            "survivorship_rules": {"path": str(survivorship_path), "sha256": sha256_file(survivorship_path), "rows": len(survivorship)},
            "hierarchy_edges": {"path": str(hierarchy_path), "sha256": sha256_file(hierarchy_path), "rows": len(hierarchy)},
            "stewardship_queue": {"path": str(stewardship_path), "sha256": sha256_file(stewardship_path), "rows": len(stewardship)},
            "external_identifiers": {"path": str(external_path), "sha256": sha256_file(external_path), "rows": len(external_ids)},
            "privacy_identity_risk": {"path": str(privacy_path), "sha256": sha256_file(privacy_path), "rows": len(privacy_risk)},
            "mdm_lineage_events": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
        },
        "outputs": {
            "candidate_scorecard": "outputs/candidate_match_scorecard_python.csv",
            "master_entity_scorecard": "outputs/master_entity_governance_scorecard_python.csv",
            "source_summary": "outputs/source_record_summary_python.csv",
            "entity_type_summary": "outputs/entity_type_summary_python.csv",
            "survivorship_summary": "outputs/survivorship_rule_summary_python.csv",
            "manifest": "outputs/mdm_entity_resolution_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "candidate_match_scorecard_python.csv", candidate_rows)
    write_csv(ROOT / "outputs" / "master_entity_governance_scorecard_python.csv", master_rows)
    write_csv(ROOT / "outputs" / "source_record_summary_python.csv", source_summary)
    write_csv(ROOT / "outputs" / "entity_type_summary_python.csv", entity_type_summary)
    write_csv(ROOT / "outputs" / "survivorship_rule_summary_python.csv", survivorship_summary)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "mdm_entity_resolution_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("MDM and entity resolution scorecard complete")
    print(json.dumps({
        "source_records": len(source_records),
        "candidate_matches": len(candidates),
        "master_entities": len(masters),
        "crosswalk_links": len(crosswalk),
        "stewardship_reviews": len(stewardship),
    }, indent=2))


if __name__ == "__main__":
    main()
