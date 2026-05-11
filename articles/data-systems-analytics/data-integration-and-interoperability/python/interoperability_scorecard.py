#!/usr/bin/env python3
"""
Python Workflow: Integration and Interoperability Scorecard

This workflow evaluates integration pathways across technical, syntactic,
semantic, identity, organizational, observability, security, and lifecycle
dimensions. It is intentionally vendor-neutral and uses only the standard
library.
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


def status_weight(status: str) -> float:
    return {"pass": 1.0, "warn": 0.6, "fail": 0.0}.get(status, 0.0)


def main() -> None:
    systems_path = ROOT / "data" / "source_systems.csv"
    mappings_path = ROOT / "data" / "schema_mappings.csv"
    crosswalk_path = ROOT / "data" / "entity_crosswalk.csv"
    checks_path = ROOT / "data" / "interoperability_checks.csv"
    lineage_path = ROOT / "data" / "lineage_events.csv"
    payloads_path = ROOT / "data" / "message_payloads.csv"

    systems = read_csv(systems_path)
    mappings = read_csv(mappings_path)
    crosswalk = read_csv(crosswalk_path)
    checks = read_csv(checks_path)
    lineage = read_csv(lineage_path)
    payloads = read_csv(payloads_path)

    check_rows = []
    layer_scores: dict[str, list[float]] = defaultdict(list)
    for row in checks:
        score = status_weight(row["status"])
        layer_scores[row["layer"]].append(score)
        check_rows.append({
            "check_id": row["check_id"],
            "layer": row["layer"],
            "check_name": row["check_name"],
            "expected_value": row["expected_value"],
            "observed_value": row["observed_value"],
            "status": row["status"],
            "score": score,
        })

    layer_summary = []
    for layer, scores in sorted(layer_scores.items()):
        layer_summary.append({
            "layer": layer,
            "check_count": len(scores),
            "average_score": round(sum(scores) / len(scores), 3),
        })

    mapping_by_risk = Counter(row["semantic_risk"] for row in mappings)
    mapping_summary = [
        {"semantic_risk": risk, "mapping_count": count}
        for risk, count in sorted(mapping_by_risk.items())
    ]

    crosswalk_confidences = [float(row["confidence"]) for row in crosswalk]
    average_crosswalk_confidence = sum(crosswalk_confidences) / len(crosswalk_confidences)

    payload_summary = {
        "total_payloads": len(payloads),
        "syntax_valid": sum(row["syntax_valid"].lower() == "true" for row in payloads),
        "semantic_valid": sum(row["semantic_valid"].lower() == "true" for row in payloads),
        "minimized_payloads": sum(row["minimized_payload"].lower() == "true" for row in payloads),
        "consumer_ready": sum(row["consumer_ready"].lower() == "true" for row in payloads),
    }

    overall_interoperability_score = round(
        0.30 * (sum(status_weight(row["status"]) for row in checks) / len(checks))
        + 0.20 * (payload_summary["semantic_valid"] / payload_summary["total_payloads"])
        + 0.15 * (payload_summary["minimized_payloads"] / payload_summary["total_payloads"])
        + 0.20 * average_crosswalk_confidence
        + 0.15 * (len(lineage) / max(len(mappings), 1)),
        3,
    )

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Integration and Interoperability",
        "workflow": "integration-interoperability-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "scorecard": {
            "overall_interoperability_score": overall_interoperability_score,
            "average_crosswalk_confidence": round(average_crosswalk_confidence, 3),
            **payload_summary,
        },
        "inputs": {
            "source_systems": {"path": str(systems_path), "sha256": sha256_file(systems_path), "rows": len(systems)},
            "schema_mappings": {"path": str(mappings_path), "sha256": sha256_file(mappings_path), "rows": len(mappings)},
            "entity_crosswalk": {"path": str(crosswalk_path), "sha256": sha256_file(crosswalk_path), "rows": len(crosswalk)},
            "interoperability_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "lineage_events": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
            "message_payloads": {"path": str(payloads_path), "sha256": sha256_file(payloads_path), "rows": len(payloads)},
        },
        "outputs": {
            "check_scorecard": "outputs/interoperability_check_scorecard_python.csv",
            "layer_summary": "outputs/interoperability_layer_summary_python.csv",
            "mapping_summary": "outputs/mapping_risk_summary_python.csv",
            "manifest": "outputs/interoperability_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "interoperability_check_scorecard_python.csv", check_rows)
    write_csv(ROOT / "outputs" / "interoperability_layer_summary_python.csv", layer_summary)
    write_csv(ROOT / "outputs" / "mapping_risk_summary_python.csv", mapping_summary)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "interoperability_manifest_python.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Integration and interoperability scorecard complete")
    print(json.dumps(manifest["scorecard"], indent=2))


if __name__ == "__main__":
    main()
