#!/usr/bin/env python3
"""
Python Workflow: ETL Transformation and Lineage Scorecard

This workflow turns raw customer/order extracts into canonical outputs,
records rejects, applies semantic mappings, simulates CDC merge readiness,
and scores transformation governance using only the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import re
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

def stable_surrogate_key(*parts: str) -> str:
    text = "|".join(parts).lower().strip()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def parse_amount(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        return 0.0

def valid_email(value: str) -> bool:
    return bool(value and re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value))

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "completed": 1.0,
        "completed_with_warning": 0.7,
        "in_review": 0.65,
        "warn": 0.45,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)

def severity_penalty(value: str) -> float:
    return {"low": 0.05, "medium": 0.10, "high": 0.20, "critical": 0.45}.get(value, 0.1)

def main() -> None:
    customers_path = ROOT / "data" / "raw_customer_extract.csv"
    orders_path = ROOT / "data" / "raw_order_extract.csv"
    mapping_path = ROOT / "data" / "status_mapping.csv"
    cdc_path = ROOT / "data" / "cdc_events.csv"
    tests_path = ROOT / "data" / "transformation_tests.csv"
    runs_path = ROOT / "data" / "orchestration_runs.csv"

    raw_customers = read_csv(customers_path)
    raw_orders = read_csv(orders_path)
    mappings = read_csv(mapping_path)
    cdc_events = read_csv(cdc_path)
    tests = read_csv(tests_path)
    runs = read_csv(runs_path)

    mapping_lookup = {
        (row["source_system"], row["source_field"], row["source_value"]): row
        for row in mappings
    }

    run_id = str(uuid.uuid4())
    loaded_at = datetime.now(timezone.utc).isoformat()

    canonical_customers = []
    rejected_records = []
    customer_key_map = {}

    for row in raw_customers:
        status_row = mapping_lookup.get((row["source_system"], "status_code", row["status_code"]))
        canonical_status = status_row["canonical_value"] if status_row else ""
        active_flag = status_row["active_flag"] if status_row else ""

        reject_reasons = []
        if not valid_email(row["email"]):
            reject_reasons.append("invalid_or_missing_email")
        if not canonical_status:
            reject_reasons.append("unmapped_customer_status")

        canonical_customer_id = stable_surrogate_key(row["email"]) if valid_email(row["email"]) else stable_surrogate_key(row["source_system"], row["source_customer_id"])
        customer_key_map[(row["source_system"], row["source_customer_id"])] = canonical_customer_id
        customer_key_map[row["source_customer_id"]] = canonical_customer_id

        if reject_reasons:
            rejected_records.append({
                "run_id": run_id,
                "entity": "customer",
                "source_system": row["source_system"],
                "source_record_id": row["source_customer_id"],
                "reject_reason": ";".join(reject_reasons),
                "record_hash": stable_surrogate_key(json.dumps(row, sort_keys=True)),
            })
            continue

        canonical_customers.append({
            "run_id": run_id,
            "canonical_customer_id": canonical_customer_id,
            "source_system": row["source_system"],
            "source_customer_id": row["source_customer_id"],
            "customer_name": row["customer_name"],
            "customer_status": canonical_status,
            "active_flag": active_flag,
            "country_code": "US" if row["country_code"] in {"US", "USA"} else row["country_code"],
            "email": row["email"].lower(),
            "source_updated_at": row["updated_at"],
            "loaded_at": loaded_at,
        })

    # Resolve cross-system customers by email into the same canonical ID.
    email_to_customer_id = {}
    for row in canonical_customers:
        email_to_customer_id.setdefault(row["email"], row["canonical_customer_id"])
    for row in canonical_customers:
        row["canonical_customer_id"] = email_to_customer_id[row["email"]]

    # Refresh key map after e-mail survivorship resolution.
    for row in canonical_customers:
        customer_key_map[(row["source_system"], row["source_customer_id"])] = row["canonical_customer_id"]
        customer_key_map[row["source_customer_id"]] = row["canonical_customer_id"]

    canonical_orders = []
    for row in raw_orders:
        status_row = mapping_lookup.get((row["source_system"], "status_code", row["status_code"]))
        canonical_status = status_row["canonical_value"] if status_row else ""
        amount = parse_amount(row["amount"])
        canonical_customer_id = customer_key_map.get((row["source_system"], row["source_customer_id"])) or customer_key_map.get(row["source_customer_id"])

        reject_reasons = []
        if not canonical_status:
            reject_reasons.append("unmapped_order_status")
        if not canonical_customer_id:
            reject_reasons.append("missing_customer_mapping")
        if canonical_status == "completed" and amount < 0:
            reject_reasons.append("completed_order_negative_amount")

        canonical_order_id = stable_surrogate_key(row["source_system"], row["source_order_id"])

        if reject_reasons:
            rejected_records.append({
                "run_id": run_id,
                "entity": "order",
                "source_system": row["source_system"],
                "source_record_id": row["source_order_id"],
                "reject_reason": ";".join(reject_reasons),
                "record_hash": stable_surrogate_key(json.dumps(row, sort_keys=True)),
            })
            continue

        canonical_orders.append({
            "run_id": run_id,
            "canonical_order_id": canonical_order_id,
            "source_system": row["source_system"],
            "source_order_id": row["source_order_id"],
            "canonical_customer_id": canonical_customer_id,
            "order_time": row["order_time"],
            "amount_usd": amount,
            "order_status": canonical_status,
            "source_updated_at": row["updated_at"],
            "loaded_at": loaded_at,
        })

    # CDC readiness summary.
    cdc_summary = []
    by_entity_operation = Counter((row["entity"], row["operation"]) for row in cdc_events)
    for (entity, operation), count in sorted(by_entity_operation.items()):
        cdc_summary.append({
            "entity": entity,
            "operation": operation,
            "event_count": count,
        })

    # Lineage records.
    lineage_rows = []
    inputs = [
        ("raw_customer_extract", customers_path, len(raw_customers)),
        ("raw_order_extract", orders_path, len(raw_orders)),
        ("status_mapping", mapping_path, len(mappings)),
        ("cdc_events", cdc_path, len(cdc_events)),
    ]
    for name, path, rows in inputs:
        lineage_rows.append({
            "run_id": run_id,
            "input_name": name,
            "input_path": str(path),
            "input_rows": rows,
            "input_sha256": sha256_file(path),
            "code_version": "local-generated-scaffold",
            "loaded_at": loaded_at,
        })

    # Test scorecard.
    test_rows = []
    test_scores = []
    for test in tests:
        score = max(0.0, status_score(test["status"]) - (severity_penalty(test["severity"]) if test["status"] != "pass" else 0.0))
        test_scores.append(score)
        test_rows.append({
            "test_id": test["test_id"],
            "test_name": test["test_name"],
            "scope": test["scope"],
            "status": test["status"],
            "severity": test["severity"],
            "score": round(score, 3),
        })

    run_scores = [status_score(row["status"]) for row in runs]
    reject_rate = len(rejected_records) / max(len(raw_customers) + len(raw_orders), 1)
    mapping_coverage = len([row for row in mappings if row["mapping_status"] == "approved"]) / max(len(mappings), 1)

    readiness = round(
        0.22 * (1.0 - min(reject_rate, 1.0))
        + 0.22 * (sum(test_scores) / max(len(test_scores), 1))
        + 0.18 * mapping_coverage
        + 0.16 * (sum(run_scores) / max(len(run_scores), 1))
        + 0.12 * (1.0 if lineage_rows else 0.0)
        + 0.10 * (1.0 if cdc_summary else 0.0),
        3,
    )

    readiness_rows = [{
        "run_id": run_id,
        "raw_customer_rows": len(raw_customers),
        "raw_order_rows": len(raw_orders),
        "canonical_customer_rows": len(canonical_customers),
        "canonical_order_rows": len(canonical_orders),
        "rejected_rows": len(rejected_records),
        "reject_rate": round(reject_rate, 4),
        "mapping_coverage": round(mapping_coverage, 4),
        "etl_readiness_score": readiness,
        "etl_readiness_gap": round(1.0 - readiness, 3),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": loaded_at,
        "article": "ETL and Data Transformation Systems",
        "workflow": "etl-transformation-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "raw_customer_extract": {"path": str(customers_path), "sha256": sha256_file(customers_path), "rows": len(raw_customers)},
            "raw_order_extract": {"path": str(orders_path), "sha256": sha256_file(orders_path), "rows": len(raw_orders)},
            "status_mapping": {"path": str(mapping_path), "sha256": sha256_file(mapping_path), "rows": len(mappings)},
            "cdc_events": {"path": str(cdc_path), "sha256": sha256_file(cdc_path), "rows": len(cdc_events)},
            "transformation_tests": {"path": str(tests_path), "sha256": sha256_file(tests_path), "rows": len(tests)},
            "orchestration_runs": {"path": str(runs_path), "sha256": sha256_file(runs_path), "rows": len(runs)},
        },
    }

    write_csv(ROOT / "outputs" / "canonical_customers_python.csv", canonical_customers)
    write_csv(ROOT / "outputs" / "canonical_orders_python.csv", canonical_orders)
    write_csv(ROOT / "outputs" / "rejected_records_python.csv", rejected_records)
    write_csv(ROOT / "outputs" / "cdc_operation_summary_python.csv", cdc_summary)
    write_csv(ROOT / "outputs" / "lineage_records_python.csv", lineage_rows)
    write_csv(ROOT / "outputs" / "transformation_test_scorecard_python.csv", test_rows)
    write_csv(ROOT / "outputs" / "etl_readiness_python.csv", readiness_rows)
    (ROOT / "outputs" / "etl_transformation_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("ETL transformation scorecard complete")
    print(json.dumps({"customers": len(canonical_customers), "orders": len(canonical_orders), "rejects": len(rejected_records), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
