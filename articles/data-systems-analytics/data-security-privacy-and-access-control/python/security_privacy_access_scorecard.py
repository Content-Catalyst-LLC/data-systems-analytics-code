#!/usr/bin/env python3
"""
Python Workflow: Security, Privacy, and Access-Control Scorecard

This workflow evaluates data assets, policies, entitlements, privacy purposes,
audit events, and flows as a connected governance system.
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


def classification_weight(classification: str) -> float:
    return {
        "public": 0.1,
        "internal": 0.35,
        "confidential": 0.7,
        "restricted": 0.9,
        "secret": 1.0,
    }.get(classification, 0.5)


def main() -> None:
    assets_path = ROOT / "data" / "data_assets.csv"
    policies_path = ROOT / "data" / "access_policies.csv"
    entitlements_path = ROOT / "data" / "entitlements.csv"
    purposes_path = ROOT / "data" / "privacy_purposes.csv"
    audits_path = ROOT / "data" / "audit_events.csv"
    flows_path = ROOT / "data" / "data_flows.csv"

    assets = read_csv(assets_path)
    policies = read_csv(policies_path)
    entitlements = read_csv(entitlements_path)
    purposes = read_csv(purposes_path)
    audits = read_csv(audits_path)
    flows = read_csv(flows_path)

    policies_by_asset = defaultdict(list)
    for policy in policies:
        policies_by_asset[policy["asset_id"]].append(policy)

    purposes_by_asset = defaultdict(list)
    for purpose in purposes:
        purposes_by_asset[purpose["asset_id"]].append(purpose)

    entitlements_by_asset = defaultdict(list)
    for entitlement in entitlements:
        entitlements_by_asset[entitlement["asset_id"]].append(entitlement)

    audit_by_asset = defaultdict(list)
    for event in audits:
        audit_by_asset[event["asset_id"]].append(event)

    flow_by_source = defaultdict(list)
    for flow in flows:
        flow_by_source[flow["source_asset"]].append(flow)

    asset_rows = []
    for asset in assets:
        asset_id = asset["asset_id"]
        sensitivity = float(asset["sensitivity_score"])
        classified_risk = classification_weight(asset["classification"])

        asset_policies = policies_by_asset[asset_id]
        allow_count = sum(policy["decision"] == "allow" for policy in asset_policies)
        deny_count = sum(policy["decision"] == "deny" for policy in asset_policies)
        deny_by_default_score = 1.0 if deny_count > 0 or asset["classification"] == "public" else 0.5

        purpose_records = purposes_by_asset[asset_id]
        minimization_score = 1.0
        purpose_score = 0.0
        if purpose_records:
            minimization_score = sum(bool_value(p["minimized_fields"]) for p in purpose_records) / len(purpose_records)
            purpose_score = sum(p["status"] == "approved" for p in purpose_records) / len(purpose_records)

        stale_entitlements = sum(e["status"] == "stale" for e in entitlements_by_asset[asset_id])
        entitlement_count = len(entitlements_by_asset[asset_id])
        entitlement_score = 1.0 if entitlement_count == 0 else max(0.0, 1.0 - stale_entitlements / entitlement_count)

        audit_events = audit_by_asset[asset_id]
        anomaly_count = sum(bool_value(e["anomaly_flag"]) for e in audit_events)
        audit_score = 1.0 if audit_events else 0.4
        anomaly_score = 1.0 if not audit_events else max(0.0, 1.0 - anomaly_count / len(audit_events))

        outbound_flows = flow_by_source[asset_id]
        protected_flows = 0
        for flow in outbound_flows:
            if bool_value(flow["masking_applied"]) or bool_value(flow["tokenization_applied"]):
                protected_flows += 1
        flow_protection_score = 1.0 if not outbound_flows else protected_flows / len(outbound_flows)

        governance_score = round(
            0.20 * deny_by_default_score
            + 0.20 * purpose_score
            + 0.15 * minimization_score
            + 0.15 * entitlement_score
            + 0.15 * audit_score
            + 0.10 * anomaly_score
            + 0.05 * flow_protection_score,
            3,
        )

        residual_risk = round(
            min(1.0, (0.55 * sensitivity + 0.45 * classified_risk) * (1.0 - governance_score)),
            3,
        )

        asset_rows.append({
            "asset_id": asset_id,
            "asset_name": asset["asset_name"],
            "classification": asset["classification"],
            "contains_personal_data": asset["contains_personal_data"],
            "contains_direct_identifiers": asset["contains_direct_identifiers"],
            "allow_policy_count": allow_count,
            "deny_policy_count": deny_count,
            "purpose_score": round(purpose_score, 3),
            "minimization_score": round(minimization_score, 3),
            "entitlement_score": round(entitlement_score, 3),
            "audit_score": round(audit_score, 3),
            "flow_protection_score": round(flow_protection_score, 3),
            "governance_score": governance_score,
            "residual_risk": residual_risk,
        })

    classification_rows = [
        {"classification": classification, "asset_count": count}
        for classification, count in sorted(Counter(a["classification"] for a in assets).items())
    ]

    entitlement_rows = [
        {"status": status, "entitlement_count": count}
        for status, count in sorted(Counter(e["status"] for e in entitlements).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Security, Privacy, and Access Control",
        "workflow": "security-privacy-access-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "data_assets": {"path": str(assets_path), "sha256": sha256_file(assets_path), "rows": len(assets)},
            "access_policies": {"path": str(policies_path), "sha256": sha256_file(policies_path), "rows": len(policies)},
            "entitlements": {"path": str(entitlements_path), "sha256": sha256_file(entitlements_path), "rows": len(entitlements)},
            "privacy_purposes": {"path": str(purposes_path), "sha256": sha256_file(purposes_path), "rows": len(purposes)},
            "audit_events": {"path": str(audits_path), "sha256": sha256_file(audits_path), "rows": len(audits)},
            "data_flows": {"path": str(flows_path), "sha256": sha256_file(flows_path), "rows": len(flows)},
        },
        "outputs": {
            "asset_scorecard": "outputs/security_privacy_access_asset_scorecard_python.csv",
            "classification_summary": "outputs/classification_summary_python.csv",
            "entitlement_summary": "outputs/entitlement_summary_python.csv",
            "manifest": "outputs/security_privacy_access_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "security_privacy_access_asset_scorecard_python.csv", asset_rows)
    write_csv(ROOT / "outputs" / "classification_summary_python.csv", classification_rows)
    write_csv(ROOT / "outputs" / "entitlement_summary_python.csv", entitlement_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "security_privacy_access_manifest_python.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Security, privacy, and access-control scorecard complete")
    print(json.dumps({
        "assets": len(assets),
        "policies": len(policies),
        "entitlements": len(entitlements),
        "audit_events": len(audits),
        "data_flows": len(flows),
    }, indent=2))


if __name__ == "__main__":
    main()
