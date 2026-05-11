#!/usr/bin/env python3
"""
Python Workflow: Data Quality Profiling, Cleaning, and Readiness Scorecard

This workflow profiles raw records, applies quality rules, standardizes fields,
detects duplicates, quarantines rejected records, records cleaning lineage,
and scores data-quality readiness using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
import statistics
import sys
import uuid
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
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

def stable_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def normalize_email(value: str) -> str:
    return value.strip().lower()

def valid_email(value: str) -> bool:
    return bool(value and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value.strip()))

def normalize_phone(value: str) -> str:
    digits = re.sub(r"\D+", "", value)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    return digits

def parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "in_review": 0.7,
        "mitigated": 0.8,
        "planned": 0.45,
        "in_progress": 0.6,
        "open": 0.35,
        "warn": 0.45,
        "fail": 0.0,
    }.get(value, 0.5)

def severity_weight(value: str) -> float:
    return {"low": 0.10, "medium": 0.20, "high": 0.35, "critical": 0.50}.get(value, 0.20)

def main() -> None:
    raw_path = ROOT / "data" / "raw_customer_records.csv"
    rules_path = ROOT / "data" / "quality_rules.csv"
    mapping_path = ROOT / "data" / "status_mapping.csv"
    root_path = ROOT / "data" / "root_cause_register.csv"
    incidents_path = ROOT / "data" / "quality_incidents.csv"

    raw = read_csv(raw_path)
    rules = read_csv(rules_path)
    mappings = read_csv(mapping_path)
    root_causes = read_csv(root_path)
    incidents = read_csv(incidents_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()
    mapping_lookup = {(row["source_system"], row["source_value"]): row["canonical_value"] for row in mappings}

    cleaned = []
    rejects = []
    lineage = []

    normalized_email_counts = Counter(normalize_email(row["email"]) for row in raw if normalize_email(row["email"]))

    for row in raw:
        reasons = []
        cleaned_email = normalize_email(row["email"])
        cleaned_phone = normalize_phone(row["phone"])
        signup_date = parse_date(row["signup_date"])
        last_updated = parse_date(row["last_updated"])
        value = parse_float(row["lifetime_value"])
        canonical_country = "US" if row["country_code"] in {"US", "USA"} else row["country_code"]
        canonical_status = mapping_lookup.get((row["source_system"], row["status"]), "")

        if not cleaned_email:
            reasons.append("missing_email")
        elif not valid_email(cleaned_email):
            reasons.append("invalid_email_format")

        if signup_date is None:
            reasons.append("invalid_signup_date")

        if value is None:
            reasons.append("invalid_lifetime_value")
        elif value < 0:
            reasons.append("negative_lifetime_value")

        if canonical_country not in {"US"}:
            reasons.append("invalid_country_code")

        if not canonical_status:
            reasons.append("unmapped_status")

        is_duplicate_email = cleaned_email and normalized_email_counts[cleaned_email] > 1
        customer_identity_key = stable_hash(cleaned_email) if cleaned_email else stable_hash(row["source_system"] + "|" + row["customer_id"])

        output = {
            "run_id": run_id,
            "record_id": row["record_id"],
            "source_system": row["source_system"],
            "source_customer_id": row["customer_id"],
            "canonical_customer_id": customer_identity_key,
            "full_name": " ".join(row["full_name"].strip().split()),
            "email": cleaned_email,
            "phone_normalized": cleaned_phone,
            "country_code": canonical_country,
            "customer_status": canonical_status,
            "signup_date": row["signup_date"],
            "last_updated": row["last_updated"],
            "lifetime_value": value if value is not None else "",
            "duplicate_email_flag": int(bool(is_duplicate_email)),
            "quality_issue_count": len(reasons),
            "cleaned_at": run_at,
        }

        lineage.append({
            "run_id": run_id,
            "record_id": row["record_id"],
            "source_system": row["source_system"],
            "raw_record_hash": stable_hash(json.dumps(row, sort_keys=True)),
            "cleaned_record_hash": stable_hash(json.dumps(output, sort_keys=True)),
            "cleaning_actions": ";".join([
                "lowercase_email" if row["email"] != cleaned_email else "",
                "normalize_phone" if row["phone"] != cleaned_phone else "",
                "standardize_country" if row["country_code"] != canonical_country else "",
                "map_status" if canonical_status else "",
            ]).strip(";"),
            "quality_issue_count": len(reasons),
        })

        if reasons:
            rejects.append({
                "run_id": run_id,
                "record_id": row["record_id"],
                "source_system": row["source_system"],
                "source_customer_id": row["customer_id"],
                "reject_or_flag_reason": ";".join(reasons),
                "repairability": "review_required" if "missing_email" in reasons or "invalid_signup_date" in reasons else "repair_possible",
                "raw_record_hash": stable_hash(json.dumps(row, sort_keys=True)),
            })

        cleaned.append(output)

    # Survivorship: one canonical row per normalized e-mail where possible.
    by_customer = defaultdict(list)
    for row in cleaned:
        by_customer[row["canonical_customer_id"]].append(row)

    survivorship_rows = []
    for customer_id, rows in sorted(by_customer.items()):
        rows_sorted = sorted(rows, key=lambda item: item["last_updated"], reverse=True)
        survivor = rows_sorted[0]
        survivorship_rows.append({
            "canonical_customer_id": customer_id,
            "survivor_record_id": survivor["record_id"],
            "source_count": len(rows),
            "survivorship_rule": "most_recent_last_updated",
            "duplicate_cluster_flag": int(len(rows) > 1),
            "survivor_source_system": survivor["source_system"],
            "survivor_email": survivor["email"],
        })

    # Rule scorecard.
    total = len(raw)
    emails_present = sum(1 for row in raw if normalize_email(row["email"]))
    valid_emails = sum(1 for row in raw if valid_email(normalize_email(row["email"])))
    valid_dates = sum(1 for row in raw if parse_date(row["signup_date"]) is not None)
    nonnegative_values = sum(1 for row in raw if (parse_float(row["lifetime_value"]) is not None and parse_float(row["lifetime_value"]) >= 0))
    allowed_countries = sum(1 for row in raw if row["country_code"] in {"US", "USA"})
    unique_normalized_emails = len(set(normalize_email(row["email"]) for row in raw if normalize_email(row["email"])))
    mapped_status = sum(1 for row in raw if (row["source_system"], row["status"]) in mapping_lookup)
    freshness_cutoff_days = 45
    today = date(2026, 5, 11)
    fresh_records = 0
    for row in raw:
        updated = parse_date(row["last_updated"])
        if updated and (today - updated).days <= freshness_cutoff_days:
            fresh_records += 1

    observed = {
        "q001": emails_present / total,
        "q002": valid_emails / total,
        "q003": valid_dates / total,
        "q004": nonnegative_values / total,
        "q005": allowed_countries / total,
        "q006": unique_normalized_emails / max(emails_present, 1),
        "q007": fresh_records / total,
        "q008": mapped_status / total,
    }

    rule_rows = []
    dimension_scores = defaultdict(list)
    for rule in rules:
        observed_value = observed.get(rule["rule_id"], 0.0)
        threshold = float(rule["threshold"])
        passed = observed_value >= threshold
        score = min(1.0, observed_value / threshold) if threshold else observed_value
        dimension_scores[rule["dimension"]].append(score)
        rule_rows.append({
            "rule_id": rule["rule_id"],
            "dimension": rule["dimension"],
            "rule_name": rule["rule_name"],
            "field_name": rule["field_name"],
            "threshold": threshold,
            "observed_value": round(observed_value, 4),
            "passed": int(passed),
            "severity": rule["severity"],
            "owner": rule["owner"],
            "status": rule["status"],
            "score": round(score, 3),
        })

    dimension_rows = []
    for dimension, scores in sorted(dimension_scores.items()):
        dimension_rows.append({
            "dimension": dimension,
            "mean_score": round(mean(scores), 3),
            "rule_count": len(scores),
        })

    incident_rows = []
    for incident in incidents:
        rule = next((r for r in rules if r["rule_id"] == incident["rule_id"]), None)
        severity = rule["severity"] if rule else "medium"
        incident_rows.append({
            "incident_id": incident["incident_id"],
            "dataset": incident["dataset"],
            "rule_id": incident["rule_id"],
            "failed_records": incident["failed_records"],
            "affected_metric": incident["affected_metric"],
            "incident_status": incident["incident_status"],
            "severity": severity,
            "risk_weight": severity_weight(severity),
        })

    root_rows = []
    for issue in root_causes:
        root_rows.append({
            "issue_id": issue["issue_id"],
            "quality_dimension": issue["quality_dimension"],
            "issue_type": issue["issue_type"],
            "affected_system": issue["affected_system"],
            "process_owner": issue["process_owner"],
            "impact_level": issue["impact_level"],
            "remediation_status": issue["remediation_status"],
            "remediation_score": status_score(issue["remediation_status"]),
        })

    reject_rate = len(rejects) / total
    rule_score = mean([row["score"] for row in rule_rows])
    root_score = mean([row["remediation_score"] for row in root_rows])
    incident_score = mean([status_score(row["incident_status"]) for row in incident_rows])
    lineage_score = 1.0 if lineage else 0.0
    survivorship_score = 1.0 if survivorship_rows else 0.0

    readiness = round(
        0.28 * rule_score
        + 0.20 * (1.0 - min(reject_rate, 1.0))
        + 0.16 * root_score
        + 0.14 * incident_score
        + 0.12 * lineage_score
        + 0.10 * survivorship_score,
        3,
    )

    readiness_rows = [{
        "run_id": run_id,
        "raw_rows": total,
        "cleaned_rows": len(cleaned),
        "flagged_or_rejected_rows": len(rejects),
        "reject_or_flag_rate": round(reject_rate, 4),
        "rule_score": round(rule_score, 3),
        "root_cause_score": round(root_score, 3),
        "incident_management_score": round(incident_score, 3),
        "lineage_score": lineage_score,
        "survivorship_score": survivorship_score,
        "data_quality_readiness_score": readiness,
        "data_quality_readiness_gap": round(1.0 - readiness, 3),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Data Cleaning and Data Quality Management",
        "workflow": "data-quality-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "raw_customer_records": {"path": str(raw_path), "sha256": sha256_file(raw_path), "rows": len(raw)},
            "quality_rules": {"path": str(rules_path), "sha256": sha256_file(rules_path), "rows": len(rules)},
            "status_mapping": {"path": str(mapping_path), "sha256": sha256_file(mapping_path), "rows": len(mappings)},
            "root_cause_register": {"path": str(root_path), "sha256": sha256_file(root_path), "rows": len(root_causes)},
            "quality_incidents": {"path": str(incidents_path), "sha256": sha256_file(incidents_path), "rows": len(incidents)},
        },
    }

    write_csv(ROOT / "outputs" / "cleaned_customer_records_python.csv", cleaned)
    write_csv(ROOT / "outputs" / "flagged_rejected_records_python.csv", rejects)
    write_csv(ROOT / "outputs" / "cleaning_lineage_python.csv", lineage)
    write_csv(ROOT / "outputs" / "survivorship_review_python.csv", survivorship_rows)
    write_csv(ROOT / "outputs" / "quality_rule_scorecard_python.csv", rule_rows)
    write_csv(ROOT / "outputs" / "quality_dimension_summary_python.csv", dimension_rows)
    write_csv(ROOT / "outputs" / "quality_incident_risk_python.csv", incident_rows)
    write_csv(ROOT / "outputs" / "root_cause_scorecard_python.csv", root_rows)
    write_csv(ROOT / "outputs" / "data_quality_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "data_quality_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Data quality scorecard complete")
    print(json.dumps({"raw_rows": total, "flagged_or_rejected_rows": len(rejects), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
