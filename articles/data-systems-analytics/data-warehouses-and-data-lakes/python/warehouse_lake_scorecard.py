#!/usr/bin/env python3
"""
Python Workflow: Warehouse, Lake, and Lakehouse Architecture Scorecard

This workflow evaluates data assets, lake zones, dimensional models, governance
controls, cost/performance metrics, lakehouse table features, workload fit, and
architecture readiness using only the Python standard library.
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

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def status_score(value: str) -> float:
    return {
        "certified": 1.0,
        "approved": 1.0,
        "pass": 1.0,
        "good": 1.0,
        "registered": 0.75,
        "acceptable": 0.70,
        "in_review": 0.60,
        "watch": 0.45,
        "warn": 0.40,
        "medium": 0.50,
        "missing": 0.10,
        "unknown": 0.15,
        "unregistered": 0.10,
        "high_risk": 0.05,
    }.get(value, 0.5)

def bool_score(value: str) -> float:
    return 1.0 if value == "1" else 0.0

def architecture_fit_score(workload: dict[str, str]) -> float:
    preferred = workload["preferred_architecture"]
    low_latency = workload["requires_low_latency_sql"] == "1"
    raw = workload["requires_raw_data_access"] == "1"
    ml = workload["requires_ml_features"] == "1"
    governance = workload["requires_strong_governance"] == "1"
    open_format = workload["requires_open_format"] == "1"

    if preferred == "warehouse":
        return 1.0 if low_latency and governance and not raw else 0.65
    if preferred == "warehouse_or_gold_lakehouse":
        return 0.95 if low_latency and governance else 0.65
    if preferred == "lakehouse_feature_layer":
        return 0.95 if raw and ml and governance and open_format else 0.60
    if preferred == "data_lake_or_lakehouse":
        return 0.85 if raw and open_format else 0.55
    if preferred == "data_lake_with_catalog":
        return 0.85 if raw and governance and open_format else 0.55
    if preferred == "warehouse_mart":
        return 0.95 if low_latency and governance else 0.65
    return 0.5

def main() -> None:
    assets_path = ROOT / "data" / "data_assets.csv"
    dims_path = ROOT / "data" / "dimensional_model_tables.csv"
    zones_path = ROOT / "data" / "lake_zones.csv"
    governance_path = ROOT / "data" / "governance_controls.csv"
    cost_path = ROOT / "data" / "cost_performance_metrics.csv"
    lakehouse_path = ROOT / "data" / "lakehouse_table_features.csv"
    workloads_path = ROOT / "data" / "workload_requirements.csv"

    assets = read_csv(assets_path)
    dims = read_csv(dims_path)
    zones = read_csv(zones_path)
    governance = read_csv(governance_path)
    costs = read_csv(cost_path)
    lakehouse = read_csv(lakehouse_path)
    workloads = read_csv(workloads_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()

    governance_by_asset = {row["asset_id"]: row for row in governance}
    cost_by_asset = {row["asset_id"]: row for row in costs}
    lakehouse_by_asset = {row["asset_id"]: row for row in lakehouse}

    asset_rows = []
    for asset in assets:
        gov = governance_by_asset.get(asset["asset_id"], {})
        cost = cost_by_asset.get(asset["asset_id"], {})
        table_features = lakehouse_by_asset.get(asset["asset_id"], {})

        metadata_score = float(gov.get("metadata_coverage", 0.0))
        lineage_score = float(gov.get("lineage_coverage", 0.0))
        owner_score = bool_score(gov.get("owner_assigned", "0"))
        classification_score = bool_score(gov.get("classification_applied", "0"))
        quality_score = status_score(gov.get("quality_status", "unknown"))
        access_score = status_score(gov.get("access_policy_status", "missing"))
        lifecycle_score = status_score(gov.get("lifecycle_status", "missing"))
        certification_score = status_score(gov.get("certification_status", asset["governance_status"]))

        scan_efficiency = float(cost.get("scan_efficiency_score", 0.0))
        cost_status = status_score(cost.get("cost_status", "watch"))
        latency = float(cost.get("p95_query_latency_seconds", 999.0))
        latency_score = max(0.0, 1.0 - min(latency / 300.0, 1.0))

        lakehouse_score = 0.0
        if table_features:
            lakehouse_score = mean([
                bool_score(table_features["acid_transactions"]),
                bool_score(table_features["schema_evolution"]),
                bool_score(table_features["time_travel"]),
                bool_score(table_features["batch_stream_unified"]),
                bool_score(table_features["metadata_scalability"]),
                status_score(table_features["table_status"]),
            ])

        asset_readiness = round(
            0.14 * metadata_score
            + 0.14 * lineage_score
            + 0.08 * owner_score
            + 0.08 * classification_score
            + 0.12 * quality_score
            + 0.10 * access_score
            + 0.08 * lifecycle_score
            + 0.12 * certification_score
            + 0.08 * scan_efficiency
            + 0.04 * cost_status
            + 0.02 * latency_score,
            3,
        )

        if asset["architecture_zone"] in {"bronze_lakehouse", "silver_lakehouse", "gold_lakehouse", "feature_store"}:
            asset_readiness = round(0.85 * asset_readiness + 0.15 * lakehouse_score, 3)

        swamp_risk = "low"
        if metadata_score < 0.60 or lineage_score < 0.50 or access_score < 0.50:
            swamp_risk = "high"
        elif metadata_score < 0.80 or lineage_score < 0.70 or certification_score < 0.60:
            swamp_risk = "medium"

        asset_rows.append({
            "asset_id": asset["asset_id"],
            "asset_name": asset["asset_name"],
            "architecture_zone": asset["architecture_zone"],
            "storage_form": asset["storage_form"],
            "schema_strategy": asset["schema_strategy"],
            "format": asset["file_or_table_format"],
            "owner": asset["owner"],
            "governance_status": asset["governance_status"],
            "row_count": asset["row_count"],
            "size_gb": asset["size_gb"],
            "freshness_hours": asset["freshness_hours"],
            "metadata_score": round(metadata_score, 3),
            "lineage_score": round(lineage_score, 3),
            "scan_efficiency_score": round(scan_efficiency, 3),
            "lakehouse_feature_score": round(lakehouse_score, 3),
            "data_swamp_risk": swamp_risk,
            "asset_readiness_score": asset_readiness,
        })

    zone_rows = []
    for zone in zones:
        assets_in_zone = [row for row in asset_rows if row["architecture_zone"] == zone["zone_name"]]
        zone_rows.append({
            "zone_id": zone["zone_id"],
            "zone_name": zone["zone_name"],
            "purpose": zone["purpose"],
            "metadata_required": zone["metadata_required"],
            "quality_gate_required": zone["quality_gate_required"],
            "retention_days": zone["retention_days"],
            "access_model": zone["access_model"],
            "declared_swamp_risk": zone["swamp_risk"],
            "status": zone["status"],
            "asset_count": len(assets_in_zone),
            "mean_asset_readiness": round(mean([row["asset_readiness_score"] for row in assets_in_zone]), 3) if assets_in_zone else "",
            "zone_control_score": round(
                0.25 * bool_score(zone["metadata_required"])
                + 0.25 * (bool_score(zone["quality_gate_required"]) if zone["zone_name"] not in {"raw_landing", "archive", "data_science_sandbox"} else 0.5)
                + 0.20 * status_score(zone["status"])
                + 0.15 * (1.0 if zone["access_model"] in {"restricted", "role_based", "project_based"} else 0.3)
                + 0.15 * (1.0 - status_score(zone["swamp_risk"]) if zone["swamp_risk"] == "high" else status_score("approved")),
                3,
            ),
        })

    dimensional_rows = []
    for row in dims:
        dimensional_rows.append({
            "table_id": row["table_id"],
            "table_name": row["table_name"],
            "model_role": row["model_role"],
            "grain": row["grain"],
            "business_process": row["business_process"],
            "conformed_dimension": row["conformed_dimension"],
            "slowly_changing_type": row["slowly_changing_type"],
            "owner": row["owner"],
            "certification_status": row["certification_status"],
            "dimensional_score": round(
                0.35 * (1.0 if row["grain"] else 0.0)
                + 0.25 * (1.0 if row["primary_key"] else 0.0)
                + 0.20 * (bool_score(row["conformed_dimension"]) if row["model_role"] == "dimension" else 0.8)
                + 0.20 * status_score(row["certification_status"]),
                3,
            ),
        })

    workload_rows = []
    for workload in workloads:
        workload_rows.append({
            "workload_id": workload["workload_id"],
            "workload_name": workload["workload_name"],
            "primary_use_case": workload["primary_use_case"],
            "preferred_architecture": workload["preferred_architecture"],
            "requires_low_latency_sql": workload["requires_low_latency_sql"],
            "requires_raw_data_access": workload["requires_raw_data_access"],
            "requires_ml_features": workload["requires_ml_features"],
            "requires_strong_governance": workload["requires_strong_governance"],
            "requires_open_format": workload["requires_open_format"],
            "architecture_fit_score": round(architecture_fit_score(workload), 3),
        })

    format_counts = Counter(asset["file_or_table_format"] for asset in assets)
    zone_counts = Counter(asset["architecture_zone"] for asset in assets)
    schema_counts = Counter(asset["schema_strategy"] for asset in assets)

    estate_summary = [{
        "evaluation_run_id": run_id,
        "asset_count": len(assets),
        "zone_count": len(zones),
        "dimensional_table_count": len(dims),
        "workload_count": len(workloads),
        "certified_asset_count": sum(1 for row in asset_rows if row["governance_status"] == "certified"),
        "high_swamp_risk_asset_count": sum(1 for row in asset_rows if row["data_swamp_risk"] == "high"),
        "mean_asset_readiness": round(mean([row["asset_readiness_score"] for row in asset_rows]), 3),
        "mean_zone_control_score": round(mean([row["zone_control_score"] for row in zone_rows if row["zone_control_score"] != ""]), 3),
        "mean_dimensional_score": round(mean([row["dimensional_score"] for row in dimensional_rows]), 3),
        "mean_workload_fit_score": round(mean([row["architecture_fit_score"] for row in workload_rows]), 3),
        "warehouse_lake_readiness_score": round(
            0.35 * mean([row["asset_readiness_score"] for row in asset_rows])
            + 0.20 * mean([row["zone_control_score"] for row in zone_rows if row["zone_control_score"] != ""])
            + 0.20 * mean([row["dimensional_score"] for row in dimensional_rows])
            + 0.15 * mean([row["architecture_fit_score"] for row in workload_rows])
            + 0.10 * (1.0 - sum(1 for row in asset_rows if row["data_swamp_risk"] == "high") / max(len(asset_rows), 1)),
            3,
        ),
        "format_counts": json.dumps(format_counts, sort_keys=True),
        "zone_counts": json.dumps(zone_counts, sort_keys=True),
        "schema_strategy_counts": json.dumps(schema_counts, sort_keys=True),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Data Warehouses and Data Lakes",
        "workflow": "warehouse-lake-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "data_assets": {"path": str(assets_path), "sha256": sha256_file(assets_path), "rows": len(assets)},
            "dimensional_model_tables": {"path": str(dims_path), "sha256": sha256_file(dims_path), "rows": len(dims)},
            "lake_zones": {"path": str(zones_path), "sha256": sha256_file(zones_path), "rows": len(zones)},
            "governance_controls": {"path": str(governance_path), "sha256": sha256_file(governance_path), "rows": len(governance)},
            "cost_performance_metrics": {"path": str(cost_path), "sha256": sha256_file(cost_path), "rows": len(costs)},
            "lakehouse_table_features": {"path": str(lakehouse_path), "sha256": sha256_file(lakehouse_path), "rows": len(lakehouse)},
            "workload_requirements": {"path": str(workloads_path), "sha256": sha256_file(workloads_path), "rows": len(workloads)},
        },
    }

    write_csv(ROOT / "outputs" / "asset_readiness_python.csv", asset_rows)
    write_csv(ROOT / "outputs" / "zone_control_scorecard_python.csv", zone_rows)
    write_csv(ROOT / "outputs" / "dimensional_model_scorecard_python.csv", dimensional_rows)
    write_csv(ROOT / "outputs" / "workload_architecture_fit_python.csv", workload_rows)
    write_csv(ROOT / "outputs" / "warehouse_lake_estate_summary_python.csv", estate_summary)
    (ROOT / "outputs" / "warehouse_lake_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Warehouse/lake architecture scorecard complete")
    print(json.dumps({"assets": len(assets), "readiness": estate_summary[0]["warehouse_lake_readiness_score"]}, indent=2))

if __name__ == "__main__":
    main()
