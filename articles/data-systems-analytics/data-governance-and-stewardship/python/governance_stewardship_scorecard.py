#!/usr/bin/env python3
"""
Python Workflow: Data Governance and Stewardship Scorecard

This workflow evaluates governance and stewardship using data assets,
roles, decision rights, policy coverage, quality issues, access reviews,
lifecycle controls, responsible-use risks, and governance events.
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


def certification_score(status: str) -> float:
    return {"certified": 1.0, "reviewed": 0.7, "uncertified": 0.2}.get(status, 0.5)


def policy_score(status: str) -> float:
    return {"enforced": 1.0, "review": 0.7, "weak": 0.3}.get(status, 0.5)


def issue_score(status: str, severity: str) -> float:
    severity_weight = {"high": 1.0, "medium": 0.7, "low": 0.4}.get(severity, 0.5)
    status_weight = {"resolved": 0.0, "in_review": 0.4, "open": 1.0}.get(status, 0.6)
    return severity_weight * status_weight


def access_score(decision: str, risk_level: str) -> float:
    if decision == "denied":
        return 1.0
    if decision == "approved_with_conditions":
        return 0.8
    if decision == "approved" and risk_level == "high":
        return 0.5
    return 0.9


def lifecycle_score(status: str) -> float:
    return {"current": 1.0, "overdue": 0.2, "missing": 0.0}.get(status, 0.5)


def responsible_use_score(status: str, severity: str) -> float:
    base = {"approved": 1.0, "in_review": 0.6, "open": 0.2}.get(status, 0.5)
    if severity == "high" and status != "approved":
        return min(base, 0.5)
    return base


def main() -> None:
    assets_path = ROOT / "data" / "data_assets.csv"
    roles_path = ROOT / "data" / "stewardship_roles.csv"
    decisions_path = ROOT / "data" / "decision_rights.csv"
    policies_path = ROOT / "data" / "policy_register.csv"
    issues_path = ROOT / "data" / "quality_issues.csv"
    access_path = ROOT / "data" / "access_reviews.csv"
    lifecycle_path = ROOT / "data" / "lifecycle_controls.csv"
    risks_path = ROOT / "data" / "responsible_use_risks.csv"
    events_path = ROOT / "data" / "governance_events.csv"

    assets = read_csv(assets_path)
    roles = read_csv(roles_path)
    decisions = read_csv(decisions_path)
    policies = read_csv(policies_path)
    issues = read_csv(issues_path)
    access = read_csv(access_path)
    lifecycle = read_csv(lifecycle_path)
    risks = read_csv(risks_path)
    events = read_csv(events_path)

    roles_by_domain = defaultdict(list)
    for row in roles:
        roles_by_domain[row["domain"]].append(row)

    policies_by_asset = defaultdict(list)
    for row in policies:
        for asset_id in row["linked_assets"].split(";"):
            policies_by_asset[asset_id].append(row)

    issues_by_asset = defaultdict(list)
    for row in issues:
        issues_by_asset[row["asset_id"]].append(row)

    access_by_asset = defaultdict(list)
    for row in access:
        access_by_asset[row["asset_id"]].append(row)

    lifecycle_by_asset = defaultdict(list)
    for row in lifecycle:
        lifecycle_by_asset[row["asset_id"]].append(row)

    risks_by_asset = defaultdict(list)
    for row in risks:
        risks_by_asset[row["asset_id"]].append(row)

    events_by_asset = defaultdict(list)
    for row in events:
        events_by_asset[row["asset_id"]].append(row)

    asset_rows = []
    for asset in assets:
        asset_id = asset["asset_id"]
        domain = asset["domain"]

        role_coverage = 1.0 if roles_by_domain[domain] or roles_by_domain["enterprise"] else 0.0
        domain_decisions = [d for d in decisions if d["domain"] in {domain, "enterprise"}]
        decision_rights_score = min(len(domain_decisions) / 2.0, 1.0)

        asset_policies = policies_by_asset[asset_id]
        policy_coverage = min(len(asset_policies) / 2.0, 1.0)
        policy_enforcement = (
            sum(policy_score(p["enforcement_status"]) for p in asset_policies) / len(asset_policies)
            if asset_policies else 0.0
        )

        asset_issues = issues_by_asset[asset_id]
        unresolved_risk = sum(issue_score(i["status"], i["severity"]) for i in asset_issues)
        issue_resolution_score = max(0.0, 1.0 - min(unresolved_risk / 2.0, 1.0))

        asset_access = access_by_asset[asset_id]
        access_review_score = (
            sum(access_score(a["decision"], a["risk_level"]) for a in asset_access) / len(asset_access)
            if asset_access else 0.7
        )

        asset_lifecycle = lifecycle_by_asset[asset_id]
        lifecycle_control_score = (
            sum(lifecycle_score(l["status"]) for l in asset_lifecycle) / len(asset_lifecycle)
            if asset_lifecycle else 0.0
        )

        asset_risks = risks_by_asset[asset_id]
        responsible_use_review = (
            sum(responsible_use_score(r["review_status"], r["severity"]) for r in asset_risks) / len(asset_risks)
            if asset_risks else 0.7
        )

        event_evidence = min(len(events_by_asset[asset_id]) / 2.0, 1.0)

        governance_maturity_score = round(
            0.12 * role_coverage
            + 0.13 * decision_rights_score
            + 0.13 * policy_coverage
            + 0.12 * policy_enforcement
            + 0.15 * issue_resolution_score
            + 0.12 * access_review_score
            + 0.10 * lifecycle_control_score
            + 0.08 * responsible_use_review
            + 0.05 * event_evidence,
            3,
        )

        asset_rows.append({
            "asset_id": asset_id,
            "asset_name": asset["asset_name"],
            "domain": domain,
            "classification": asset["classification"],
            "criticality": asset["criticality"],
            "certification_status": asset["certification_status"],
            "role_coverage": round(role_coverage, 3),
            "decision_rights_score": round(decision_rights_score, 3),
            "policy_coverage": round(policy_coverage, 3),
            "policy_enforcement": round(policy_enforcement, 3),
            "issue_resolution_score": round(issue_resolution_score, 3),
            "access_review_score": round(access_review_score, 3),
            "lifecycle_control_score": round(lifecycle_control_score, 3),
            "responsible_use_review": round(responsible_use_review, 3),
            "event_evidence": round(event_evidence, 3),
            "governance_maturity_score": governance_maturity_score,
            "governance_gap": round(1.0 - governance_maturity_score, 3),
        })

    policy_rows = [
        {"policy_domain": domain, "policy_count": count}
        for domain, count in sorted(Counter(p["policy_domain"] for p in policies).items())
    ]

    issue_rows = [
        {"status": status, "issue_count": count}
        for status, count in sorted(Counter(i["status"] for i in issues).items())
    ]

    access_rows = [
        {"decision": decision, "access_review_count": count}
        for decision, count in sorted(Counter(a["decision"] for a in access).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Governance and Stewardship",
        "workflow": "governance-stewardship-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "data_assets": {"path": str(assets_path), "sha256": sha256_file(assets_path), "rows": len(assets)},
            "stewardship_roles": {"path": str(roles_path), "sha256": sha256_file(roles_path), "rows": len(roles)},
            "decision_rights": {"path": str(decisions_path), "sha256": sha256_file(decisions_path), "rows": len(decisions)},
            "policy_register": {"path": str(policies_path), "sha256": sha256_file(policies_path), "rows": len(policies)},
            "quality_issues": {"path": str(issues_path), "sha256": sha256_file(issues_path), "rows": len(issues)},
            "access_reviews": {"path": str(access_path), "sha256": sha256_file(access_path), "rows": len(access)},
            "lifecycle_controls": {"path": str(lifecycle_path), "sha256": sha256_file(lifecycle_path), "rows": len(lifecycle)},
            "responsible_use_risks": {"path": str(risks_path), "sha256": sha256_file(risks_path), "rows": len(risks)},
            "governance_events": {"path": str(events_path), "sha256": sha256_file(events_path), "rows": len(events)},
        },
        "outputs": {
            "asset_scorecard": "outputs/governance_stewardship_scorecard_python.csv",
            "policy_summary": "outputs/policy_domain_summary_python.csv",
            "issue_summary": "outputs/quality_issue_status_summary_python.csv",
            "access_summary": "outputs/access_decision_summary_python.csv",
            "manifest": "outputs/governance_stewardship_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "governance_stewardship_scorecard_python.csv", asset_rows)
    write_csv(ROOT / "outputs" / "policy_domain_summary_python.csv", policy_rows)
    write_csv(ROOT / "outputs" / "quality_issue_status_summary_python.csv", issue_rows)
    write_csv(ROOT / "outputs" / "access_decision_summary_python.csv", access_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "governance_stewardship_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Data governance and stewardship scorecard complete")
    print(json.dumps({
        "assets": len(assets),
        "roles": len(roles),
        "decision_rights": len(decisions),
        "policies": len(policies),
        "quality_issues": len(issues),
        "access_reviews": len(access),
    }, indent=2))


if __name__ == "__main__":
    main()
