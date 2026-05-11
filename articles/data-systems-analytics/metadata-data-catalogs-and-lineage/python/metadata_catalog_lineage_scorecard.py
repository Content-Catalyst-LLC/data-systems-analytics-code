#!/usr/bin/env python3
"""
Python Workflow: Metadata, Catalog, and Lineage Trust Scorecard

This workflow evaluates data assets using metadata completeness,
catalog visibility, glossary alignment, lineage depth, provenance completeness,
policy enforcement, quality signals, and usage context.
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


def quality_score(status: str) -> float:
    return {"approved": 1.0, "review": 0.7, "stale": 0.4, "missing": 0.0}.get(status, 0.5)


def signal_score(status: str) -> float:
    return {"pass": 1.0, "normal": 1.0, "warn": 0.6, "fail": 0.0}.get(status, 0.5)


def certification_score(status: str) -> float:
    return {"certified": 1.0, "reviewed": 0.7, "uncertified": 0.2}.get(status, 0.5)


def enforcement_score(status: str) -> float:
    return {"enforced": 1.0, "review": 0.7, "weak": 0.3}.get(status, 0.5)


def main() -> None:
    assets_path = ROOT / "data" / "data_assets.csv"
    elements_path = ROOT / "data" / "metadata_elements.csv"
    catalog_path = ROOT / "data" / "catalog_entries.csv"
    glossary_path = ROOT / "data" / "glossary_terms.csv"
    lineage_path = ROOT / "data" / "lineage_edges.csv"
    provenance_path = ROOT / "data" / "provenance_events.csv"
    policy_path = ROOT / "data" / "policy_tags.csv"
    signals_path = ROOT / "data" / "quality_signals.csv"
    usage_path = ROOT / "data" / "catalog_usage.csv"

    assets = read_csv(assets_path)
    elements = read_csv(elements_path)
    catalog = read_csv(catalog_path)
    glossary = read_csv(glossary_path)
    lineage = read_csv(lineage_path)
    provenance = read_csv(provenance_path)
    policies = read_csv(policy_path)
    signals = read_csv(signals_path)
    usage = read_csv(usage_path)

    elements_by_asset = defaultdict(list)
    for row in elements:
        elements_by_asset[row["asset_id"]].append(row)

    catalog_by_asset = {row["asset_id"]: row for row in catalog}

    glossary_by_asset = defaultdict(list)
    for row in glossary:
        glossary_by_asset[row["linked_asset_id"]].append(row)

    lineage_by_asset = defaultdict(list)
    for row in lineage:
        lineage_by_asset[row["upstream_asset"]].append(row)
        lineage_by_asset[row["downstream_asset"]].append(row)

    provenance_by_asset = defaultdict(list)
    for row in provenance:
        provenance_by_asset[row["asset_id"]].append(row)

    policy_by_asset = defaultdict(list)
    for row in policies:
        policy_by_asset[row["asset_id"]].append(row)

    signals_by_asset = defaultdict(list)
    for row in signals:
        signals_by_asset[row["asset_id"]].append(row)

    usage_by_asset = {row["asset_id"]: row for row in usage}

    asset_rows = []
    for asset in assets:
        asset_id = asset["asset_id"]

        asset_elements = elements_by_asset[asset_id]
        metadata_completeness = min(len(asset_elements) / 3.0, 1.0)
        metadata_quality = sum(quality_score(e["quality_status"]) for e in asset_elements) / len(asset_elements) if asset_elements else 0.0

        cat = catalog_by_asset.get(asset_id)
        catalog_score = 0.0
        if cat:
            catalog_flags = [
                bool_value(cat["discoverable"]),
                bool_value(cat["description_complete"]),
                bool_value(cat["owner_visible"]),
                bool_value(cat["quality_visible"]),
                bool_value(cat["lineage_visible"]),
                bool_value(cat["policy_visible"]),
                bool_value(cat["usage_visible"]),
            ]
            catalog_score = sum(catalog_flags) / len(catalog_flags)

        glossary_score = 1.0 if glossary_by_asset[asset_id] else 0.0

        lineage_edges = lineage_by_asset[asset_id]
        lineage_score = min(len(lineage_edges) / 2.0, 1.0)
        column_lineage_present = any(edge["lineage_granularity"] == "column" for edge in lineage_edges)
        lineage_depth_score = min(
            0.60 * lineage_score + 0.40 * float(column_lineage_present),
            1.0,
        )

        prov_records = provenance_by_asset[asset_id]
        provenance_score = (
            sum(bool_value(p["provenance_complete"]) for p in prov_records) / len(prov_records)
            if prov_records else 0.0
        )

        policy_records = policy_by_asset[asset_id]
        policy_score = (
            sum(enforcement_score(p["enforcement_status"]) for p in policy_records) / len(policy_records)
            if policy_records else 0.0
        )

        asset_signals = signals_by_asset[asset_id]
        quality_signal_score = (
            sum(signal_score(s["status"]) for s in asset_signals) / len(asset_signals)
            if asset_signals else 0.6
        )

        use = usage_by_asset.get(asset_id)
        adoption_score = 0.0
        if use:
            total = int(use["search_count"]) + int(use["view_count"]) + int(use["query_count"])
            adoption_score = min(total / 300.0, 1.0)

        metadata_trust_score = round(
            0.15 * metadata_completeness
            + 0.15 * metadata_quality
            + 0.15 * catalog_score
            + 0.10 * glossary_score
            + 0.15 * lineage_depth_score
            + 0.10 * provenance_score
            + 0.10 * policy_score
            + 0.05 * quality_signal_score
            + 0.05 * adoption_score,
            3,
        )

        evidence_gap = round(1.0 - metadata_trust_score, 3)

        asset_rows.append({
            "asset_id": asset_id,
            "asset_name": asset["asset_name"],
            "domain": asset["domain"],
            "asset_type": asset["asset_type"],
            "classification": asset["classification"],
            "certification_status": asset["certification_status"],
            "metadata_completeness": round(metadata_completeness, 3),
            "metadata_quality": round(metadata_quality, 3),
            "catalog_score": round(catalog_score, 3),
            "glossary_score": round(glossary_score, 3),
            "lineage_depth_score": round(lineage_depth_score, 3),
            "provenance_score": round(provenance_score, 3),
            "policy_score": round(policy_score, 3),
            "quality_signal_score": round(quality_signal_score, 3),
            "adoption_score": round(adoption_score, 3),
            "metadata_trust_score": metadata_trust_score,
            "evidence_gap": evidence_gap,
        })

    type_rows = [
        {"metadata_type": metadata_type, "element_count": count}
        for metadata_type, count in sorted(Counter(e["metadata_type"] for e in elements).items())
    ]

    lineage_rows = [
        {"lineage_granularity": granularity, "edge_count": count}
        for granularity, count in sorted(Counter(e["lineage_granularity"] for e in lineage).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Metadata, Data Catalogs, and Lineage",
        "workflow": "metadata-catalog-lineage-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "data_assets": {"path": str(assets_path), "sha256": sha256_file(assets_path), "rows": len(assets)},
            "metadata_elements": {"path": str(elements_path), "sha256": sha256_file(elements_path), "rows": len(elements)},
            "catalog_entries": {"path": str(catalog_path), "sha256": sha256_file(catalog_path), "rows": len(catalog)},
            "glossary_terms": {"path": str(glossary_path), "sha256": sha256_file(glossary_path), "rows": len(glossary)},
            "lineage_edges": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
            "provenance_events": {"path": str(provenance_path), "sha256": sha256_file(provenance_path), "rows": len(provenance)},
            "policy_tags": {"path": str(policy_path), "sha256": sha256_file(policy_path), "rows": len(policies)},
            "quality_signals": {"path": str(signals_path), "sha256": sha256_file(signals_path), "rows": len(signals)},
            "catalog_usage": {"path": str(usage_path), "sha256": sha256_file(usage_path), "rows": len(usage)},
        },
        "outputs": {
            "asset_scorecard": "outputs/metadata_catalog_lineage_scorecard_python.csv",
            "metadata_type_summary": "outputs/metadata_type_summary_python.csv",
            "lineage_granularity_summary": "outputs/lineage_granularity_summary_python.csv",
            "manifest": "outputs/metadata_catalog_lineage_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "metadata_catalog_lineage_scorecard_python.csv", asset_rows)
    write_csv(ROOT / "outputs" / "metadata_type_summary_python.csv", type_rows)
    write_csv(ROOT / "outputs" / "lineage_granularity_summary_python.csv", lineage_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "metadata_catalog_lineage_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Metadata, catalog, and lineage scorecard complete")
    print(json.dumps({
        "assets": len(assets),
        "metadata_elements": len(elements),
        "lineage_edges": len(lineage),
        "provenance_events": len(provenance),
    }, indent=2))


if __name__ == "__main__":
    main()
