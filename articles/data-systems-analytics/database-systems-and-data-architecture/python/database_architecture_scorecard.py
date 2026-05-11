#!/usr/bin/env python3
"""
Python Workflow: Database Systems and Data Architecture Readiness Scorecard

This workflow evaluates system inventory, schema assets, workloads, governance,
recovery plans, lineage edges, architecture risks, and estate-readiness scoring
using only the Python standard library.
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
        "complete": 1.0,
        "registered": 0.75,
        "in_review": 0.60,
        "watch": 0.45,
        "warn": 0.40,
        "planned": 0.35,
        "partial": 0.45,
        "missing": 0.10,
        "failed": 0.0,
    }.get(value, 0.5)

def severity_weight(value: str) -> float:
    return {"low": 0.10, "medium": 0.25, "high": 0.45, "critical": 0.65}.get(value, 0.25)

def likelihood_weight(value: str) -> float:
    return {"low": 0.20, "medium": 0.50, "high": 0.80}.get(value, 0.50)

def bool_score(value: str) -> float:
    return 1.0 if value == "1" else 0.0

def main() -> None:
    systems_path = ROOT / "data" / "system_inventory.csv"
    assets_path = ROOT / "data" / "schema_assets.csv"
    workloads_path = ROOT / "data" / "workload_catalog.csv"
    governance_path = ROOT / "data" / "governance_controls.csv"
    recovery_path = ROOT / "data" / "recovery_plans.csv"
    lineage_path = ROOT / "data" / "integration_lineage.csv"
    risks_path = ROOT / "data" / "architecture_risks.csv"

    systems = read_csv(systems_path)
    assets = read_csv(assets_path)
    workloads = read_csv(workloads_path)
    governance = read_csv(governance_path)
    recovery = read_csv(recovery_path)
    lineage = read_csv(lineage_path)
    risks = read_csv(risks_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()

    governance_by_system = {row["system_id"]: row for row in governance}
    recovery_by_system = {row["system_id"]: row for row in recovery}
    assets_by_system = defaultdict(list)
    for asset in assets:
        assets_by_system[asset["system_id"]].append(asset)
    risk_by_system = defaultdict(list)
    for risk in risks:
        risk_by_system[risk["system_id"]].append(risk)
    lineage_edges_by_system = defaultdict(list)
    for edge in lineage:
        lineage_edges_by_system[edge["source_system"]].append(edge)
        lineage_edges_by_system[edge["target_system"]].append(edge)

    system_rows = []
    for system in systems:
        gov = governance_by_system.get(system["system_id"], {})
        rec = recovery_by_system.get(system["system_id"], {})
        system_assets = assets_by_system[system["system_id"]]
        system_risks = risk_by_system[system["system_id"]]
        system_edges = lineage_edges_by_system[system["system_name"]]

        metadata_score = float(gov.get("metadata_coverage", 0.0))
        lineage_score = float(gov.get("lineage_coverage", 0.0))
        owner_score = bool_score(gov.get("owner_assigned", "0"))
        classification_score = bool_score(gov.get("classification_applied", "0"))
        access_score = status_score(gov.get("access_policy_status", "missing"))
        backup_score = status_score(gov.get("backup_status", "missing"))
        recovery_test_score = status_score(gov.get("recovery_test_status", "missing"))
        retention_score = status_score(gov.get("retention_policy_status", "missing"))
        quality_score = status_score(gov.get("quality_gate_status", "missing"))
        certification_score = status_score(gov.get("certification_status", system["certification_status"]))

        rpo = float(rec.get("recovery_point_objective_minutes", 9999))
        rto = float(rec.get("recovery_time_objective_minutes", 9999))
        backup_age = float(rec.get("last_backup_age_minutes", 9999))
        restore_days = float(rec.get("last_restore_test_days_ago", 9999))
        rpo_score = 1.0 if backup_age <= rpo else max(0.0, 1.0 - min((backup_age - rpo) / max(rpo, 1), 1.0))
        rto_score = 1.0 if status_score(rec.get("status", "missing")) >= 0.75 else status_score(rec.get("status", "missing"))
        restore_score = max(0.0, 1.0 - min(restore_days / 120.0, 1.0))

        asset_score = mean([
            0.18 * (1.0 if a["grain"] else 0.0)
            + 0.16 * (1.0 if a["primary_key"] else 0.0)
            + 0.16 * min(1.0, int(a["constraint_count"]) / 6.0)
            + 0.14 * status_score(a["lineage_status"])
            + 0.14 * status_score(a["quality_status"])
            + 0.12 * status_score(a["access_status"])
            + 0.10 * status_score(a["lifecycle_status"])
            for a in system_assets
        ]) if system_assets else 0.60

        edge_score = mean([
            0.30 * status_score(edge["lineage_visibility"])
            + 0.25 * status_score(edge["quality_gate"])
            + 0.25 * status_score(edge["contract_status"])
            + 0.20 * status_score(edge["status"])
            for edge in system_edges
        ]) if system_edges else 0.60

        risk_penalty = min(0.40, sum(severity_weight(r["severity"]) * likelihood_weight(r["likelihood"]) for r in system_risks) / 4.0)

        system_readiness = round(max(0.0,
            0.13 * metadata_score
            + 0.13 * lineage_score
            + 0.07 * owner_score
            + 0.06 * classification_score
            + 0.09 * access_score
            + 0.08 * backup_score
            + 0.08 * recovery_test_score
            + 0.07 * retention_score
            + 0.08 * quality_score
            + 0.08 * certification_score
            + 0.08 * asset_score
            + 0.08 * edge_score
            + 0.04 * rpo_score
            + 0.04 * rto_score
            + 0.04 * restore_score
            - risk_penalty
        ), 3)

        system_rows.append({
            "system_id": system["system_id"],
            "system_name": system["system_name"],
            "system_type": system["system_type"],
            "storage_model": system["storage_model"],
            "primary_workload": system["primary_workload"],
            "owner": system["owner"],
            "criticality": system["criticality"],
            "records_millions": system["records_millions"],
            "data_volume_gb": system["data_volume_gb"],
            "availability_target": system["availability_target"],
            "asset_count": len(system_assets),
            "integration_edge_count": len(system_edges),
            "risk_count": len(system_risks),
            "metadata_score": round(metadata_score, 3),
            "lineage_score": round(lineage_score, 3),
            "asset_score": round(asset_score, 3),
            "recovery_score": round(mean([rpo_score, rto_score, restore_score]), 3),
            "risk_penalty": round(risk_penalty, 3),
            "system_readiness_score": system_readiness,
        })

    asset_rows = []
    for asset in assets:
        asset_rows.append({
            "asset_id": asset["asset_id"],
            "system_id": asset["system_id"],
            "asset_name": asset["asset_name"],
            "asset_type": asset["asset_type"],
            "grain": asset["grain"],
            "primary_key": asset["primary_key"],
            "foreign_key_count": asset["foreign_key_count"],
            "constraint_count": asset["constraint_count"],
            "owner": asset["owner"],
            "classification": asset["classification"],
            "lineage_status": asset["lineage_status"],
            "quality_status": asset["quality_status"],
            "access_status": asset["access_status"],
            "lifecycle_status": asset["lifecycle_status"],
            "asset_architecture_score": round(
                0.18 * (1.0 if asset["grain"] else 0.0)
                + 0.18 * (1.0 if asset["primary_key"] else 0.0)
                + 0.12 * min(1.0, int(asset["foreign_key_count"]) / 3.0)
                + 0.12 * min(1.0, int(asset["constraint_count"]) / 8.0)
                + 0.14 * status_score(asset["lineage_status"])
                + 0.12 * status_score(asset["quality_status"])
                + 0.08 * status_score(asset["access_status"])
                + 0.06 * status_score(asset["lifecycle_status"]),
                3,
            ),
        })

    workload_rows = []
    for workload in workloads:
        latency = float(workload["latency_requirement_ms"])
        throughput = float(workload["throughput_requirement_per_minute"])
        latency_complexity = 1.0 if latency >= 1000 else 0.75
        throughput_complexity = 1.0 - min(throughput / 50000.0, 0.6)
        workload_rows.append({
            "workload_id": workload["workload_id"],
            "workload_name": workload["workload_name"],
            "workload_type": workload["workload_type"],
            "systems_used": workload["systems_used"],
            "latency_requirement_ms": latency,
            "throughput_requirement_per_minute": throughput,
            "consistency_need": workload["consistency_need"],
            "availability_need": workload["availability_need"],
            "governance_need": workload["governance_need"],
            "status": workload["status"],
            "workload_fit_score": round(
                0.30 * status_score(workload["status"])
                + 0.20 * latency_complexity
                + 0.20 * throughput_complexity
                + 0.15 * (1.0 if workload["governance_need"] in {"high", "critical"} else 0.7)
                + 0.15 * (1.0 if workload["availability_need"] in {"high", "critical"} else 0.7),
                3,
            ),
        })

    lineage_rows = []
    for edge in lineage:
        lineage_rows.append({
            "edge_id": edge["edge_id"],
            "source_system": edge["source_system"],
            "target_system": edge["target_system"],
            "flow_type": edge["flow_type"],
            "frequency": edge["frequency"],
            "lineage_visibility": edge["lineage_visibility"],
            "transformation_owner": edge["transformation_owner"],
            "quality_gate": edge["quality_gate"],
            "contract_status": edge["contract_status"],
            "status": edge["status"],
            "lineage_edge_score": round(
                0.30 * status_score(edge["lineage_visibility"])
                + 0.25 * status_score(edge["quality_gate"])
                + 0.25 * status_score(edge["contract_status"])
                + 0.20 * status_score(edge["status"]),
                3,
            ),
        })

    risk_rows = []
    for risk in risks:
        risk_score = severity_weight(risk["severity"]) * likelihood_weight(risk["likelihood"])
        risk_rows.append({
            "risk_id": risk["risk_id"],
            "risk_area": risk["risk_area"],
            "system_id": risk["system_id"],
            "description": risk["description"],
            "severity": risk["severity"],
            "likelihood": risk["likelihood"],
            "owner": risk["owner"],
            "status": risk["status"],
            "risk_score": round(risk_score, 3),
            "risk_resolution_score": round(status_score(risk["status"]) * (1.0 - min(risk_score, 0.8) / 2.0), 3),
        })

    estate_readiness = round(
        0.35 * mean([row["system_readiness_score"] for row in system_rows])
        + 0.20 * mean([row["asset_architecture_score"] for row in asset_rows])
        + 0.18 * mean([row["workload_fit_score"] for row in workload_rows])
        + 0.15 * mean([row["lineage_edge_score"] for row in lineage_rows])
        + 0.12 * mean([row["risk_resolution_score"] for row in risk_rows]),
        3,
    )

    summary_rows = [{
        "evaluation_run_id": run_id,
        "system_count": len(systems),
        "asset_count": len(assets),
        "workload_count": len(workloads),
        "governance_control_count": len(governance),
        "recovery_plan_count": len(recovery),
        "lineage_edge_count": len(lineage),
        "architecture_risk_count": len(risks),
        "mean_system_readiness": round(mean([row["system_readiness_score"] for row in system_rows]), 3),
        "mean_asset_architecture_score": round(mean([row["asset_architecture_score"] for row in asset_rows]), 3),
        "mean_workload_fit_score": round(mean([row["workload_fit_score"] for row in workload_rows]), 3),
        "mean_lineage_edge_score": round(mean([row["lineage_edge_score"] for row in lineage_rows]), 3),
        "mean_risk_resolution_score": round(mean([row["risk_resolution_score"] for row in risk_rows]), 3),
        "database_architecture_readiness_score": estate_readiness,
        "database_architecture_readiness_gap": round(1.0 - estate_readiness, 3),
        "system_type_counts": json.dumps(Counter(s["system_type"] for s in systems), sort_keys=True),
        "storage_model_counts": json.dumps(Counter(s["storage_model"] for s in systems), sort_keys=True),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Database Systems and Data Architecture",
        "workflow": "database-architecture-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "system_inventory": {"path": str(systems_path), "sha256": sha256_file(systems_path), "rows": len(systems)},
            "schema_assets": {"path": str(assets_path), "sha256": sha256_file(assets_path), "rows": len(assets)},
            "workload_catalog": {"path": str(workloads_path), "sha256": sha256_file(workloads_path), "rows": len(workloads)},
            "governance_controls": {"path": str(governance_path), "sha256": sha256_file(governance_path), "rows": len(governance)},
            "recovery_plans": {"path": str(recovery_path), "sha256": sha256_file(recovery_path), "rows": len(recovery)},
            "integration_lineage": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
            "architecture_risks": {"path": str(risks_path), "sha256": sha256_file(risks_path), "rows": len(risks)},
        },
    }

    write_csv(ROOT / "outputs" / "system_readiness_python.csv", system_rows)
    write_csv(ROOT / "outputs" / "asset_architecture_scorecard_python.csv", asset_rows)
    write_csv(ROOT / "outputs" / "workload_fit_python.csv", workload_rows)
    write_csv(ROOT / "outputs" / "lineage_edge_scorecard_python.csv", lineage_rows)
    write_csv(ROOT / "outputs" / "architecture_risk_scorecard_python.csv", risk_rows)
    write_csv(ROOT / "outputs" / "database_architecture_estate_summary_python.csv", summary_rows)
    (ROOT / "outputs" / "database_architecture_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Database architecture scorecard complete")
    print(json.dumps({"systems": len(systems), "assets": len(assets), "readiness": estate_readiness}, indent=2))

if __name__ == "__main__":
    main()
