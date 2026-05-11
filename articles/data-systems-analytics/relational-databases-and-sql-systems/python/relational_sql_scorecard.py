#!/usr/bin/env python3
"""
Python Workflow: Relational Schema, SQL Workload, Integrity, and Readiness Scorecard

This workflow evaluates table grains, constraints, normalization checks, indexes,
query workloads, transaction evidence, access controls, integrity incidents, and
relational SQL readiness using only the Python standard library.
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
        "committed": 1.0,
        "resolved": 0.9,
        "registered": 0.75,
        "in_review": 0.60,
        "watch": 0.45,
        "warn": 0.40,
        "planned": 0.35,
        "rolled_back": 0.25,
        "missing": 0.10,
        "failed": 0.0,
    }.get(value, 0.5)

def severity_weight(value: str) -> float:
    return {"low": 0.05, "medium": 0.15, "high": 0.30, "critical": 0.50}.get(value, 0.15)

def bool_score(value: str) -> float:
    return 1.0 if value == "1" else 0.0

def main() -> None:
    schema_path = ROOT / "data" / "relational_schema_inventory.csv"
    constraints_path = ROOT / "data" / "constraint_inventory.csv"
    workload_path = ROOT / "data" / "query_workload.csv"
    indexes_path = ROOT / "data" / "index_inventory.csv"
    normalization_path = ROOT / "data" / "normalization_checks.csv"
    txn_path = ROOT / "data" / "transaction_log_sample.csv"
    access_path = ROOT / "data" / "access_controls.csv"
    incidents_path = ROOT / "data" / "integrity_incidents.csv"

    schema = read_csv(schema_path)
    constraints = read_csv(constraints_path)
    workloads = read_csv(workload_path)
    indexes = read_csv(indexes_path)
    normalization = read_csv(normalization_path)
    transactions = read_csv(txn_path)
    access = read_csv(access_path)
    incidents = read_csv(incidents_path)

    run_id = str(uuid.uuid4())
    run_at = datetime.now(timezone.utc).isoformat()

    constraints_by_table = defaultdict(list)
    for constraint in constraints:
        constraints_by_table[constraint["table_name"]].append(constraint)

    indexes_by_table = defaultdict(list)
    for index in indexes:
        indexes_by_table[index["table_name"]].append(index)

    normalization_by_table = {row["table_name"]: row for row in normalization}
    incident_by_table = defaultdict(list)
    for incident in incidents:
        incident_by_table[incident["table_name"]].append(incident)

    table_rows = []
    for table in schema:
        table_constraints = constraints_by_table[table["table_name"]]
        table_indexes = indexes_by_table[table["table_name"]]
        norm = normalization_by_table.get(table["table_name"], {})
        table_incidents = incident_by_table[table["table_name"]]

        has_pk = any(c["constraint_type"] == "primary_key" for c in table_constraints)
        fk_count = sum(1 for c in table_constraints if c["constraint_type"] == "foreign_key")
        check_count = sum(1 for c in table_constraints if c["constraint_type"] == "check")
        approved_constraint_share = mean([status_score(c["status"]) for c in table_constraints])
        index_status_score = mean([status_score(i["status"]) for i in table_indexes])
        normalization_score = status_score(norm.get("status", "missing"))
        incident_penalty = min(0.5, sum(severity_weight(i["severity"]) for i in table_incidents))

        table_score = round(
            0.18 * int(has_pk)
            + 0.16 * approved_constraint_share
            + 0.12 * min(1.0, fk_count / 2.0 if table["entity_type"] != "entity" else 1.0)
            + 0.10 * min(1.0, check_count / 2.0)
            + 0.16 * index_status_score
            + 0.14 * normalization_score
            + 0.14 * status_score(table["certification_status"])
            - incident_penalty,
            3,
        )
        table_score = max(0.0, table_score)

        table_rows.append({
            "table_id": table["table_id"],
            "table_name": table["table_name"],
            "entity_type": table["entity_type"],
            "grain": table["grain"],
            "primary_key": table["primary_key"],
            "owner": table["owner"],
            "normalization_target": table["normalization_target"],
            "row_count": table["row_count"],
            "constraint_count": len(table_constraints),
            "foreign_key_count": fk_count,
            "check_constraint_count": check_count,
            "index_count": len(table_indexes),
            "normalization_status": norm.get("status", ""),
            "incident_count": len(table_incidents),
            "certification_status": table["certification_status"],
            "table_readiness_score": table_score,
        })

    constraint_rows = []
    for constraint in constraints:
        relationship_complete = 1.0
        if constraint["constraint_type"] == "foreign_key":
            relationship_complete = 1.0 if constraint["referenced_table"] and constraint["referenced_column"] else 0.0
        constraint_rows.append({
            "constraint_id": constraint["constraint_id"],
            "table_name": constraint["table_name"],
            "column_name": constraint["column_name"],
            "constraint_type": constraint["constraint_type"],
            "referenced_table": constraint["referenced_table"],
            "severity": constraint["severity"],
            "status": constraint["status"],
            "constraint_score": round(
                0.45 * status_score(constraint["status"])
                + 0.25 * relationship_complete
                + 0.15 * (1.0 - severity_weight(constraint["severity"]))
                + 0.15 * (1.0 if constraint["rule_expression"] else 0.0),
                3,
            ),
        })

    # Query/index fit.
    index_columns_by_table = defaultdict(list)
    for index in indexes:
        for col in index["columns"].replace('"', "").split(";"):
            index_columns_by_table[index["table_name"]].append(col.strip())

    query_rows = []
    for query in workloads:
        tables = query["primary_tables"].replace('"', "").split(";")
        filter_cols = [c for c in query["filter_columns"].replace('"', "").split(";") if c]
        p95 = float(query["p95_latency_ms"])
        expected = float(query["expected_latency_ms"])
        latency_score = max(0.0, min(1.0, expected / p95 if p95 else 1.0))
        indexed_filters = 0
        for col in filter_cols:
            if any(col in index["columns"] for index in indexes if index["table_name"] in tables):
                indexed_filters += 1
        index_fit = indexed_filters / max(len(filter_cols), 1)
        criticality_modifier = 1.0 - severity_weight(query["criticality"])
        query_rows.append({
            "query_id": query["query_id"],
            "workload_name": query["workload_name"],
            "query_type": query["query_type"],
            "primary_tables": query["primary_tables"],
            "join_count": query["join_count"],
            "filter_columns": query["filter_columns"],
            "expected_latency_ms": expected,
            "p95_latency_ms": p95,
            "execution_count_per_day": query["execution_count_per_day"],
            "index_fit_score": round(index_fit, 3),
            "latency_score": round(latency_score, 3),
            "status": query["status"],
            "query_readiness_score": round(0.35 * index_fit + 0.35 * latency_score + 0.20 * status_score(query["status"]) + 0.10 * criticality_modifier, 3),
        })

    transaction_rows = []
    for txn in transactions:
        latency = float(txn["latency_ms"])
        latency_score = max(0.0, 1.0 - min(latency / 1000.0, 1.0))
        retry_penalty = min(0.4, int(txn["deadlock_retry_count"]) * 0.15)
        transaction_rows.append({
            "txn_id": txn["txn_id"],
            "tables_touched": txn["tables_touched"],
            "isolation_level": txn["isolation_level"],
            "result": txn["result"],
            "rollback_flag": txn["rollback_flag"],
            "deadlock_retry_count": txn["deadlock_retry_count"],
            "latency_ms": latency,
            "transaction_score": round(max(0.0, 0.45 * status_score(txn["result"]) + 0.25 * latency_score + 0.20 * (1.0 - bool_score(txn["rollback_flag"])) + 0.10 * (1.0 - retry_penalty)), 3),
        })

    access_rows = []
    for grant in access:
        privilege_breadth = 0.4 if grant["privilege"] == "ALL" else (0.25 if "UPDATE" in grant["privilege"] else 0.10)
        masking_fit = 1.0 if grant["masking_required"] == "0" or grant["row_level_security"] == "1" else 0.50
        access_rows.append({
            "grant_id": grant["grant_id"],
            "role_name": grant["role_name"],
            "table_name": grant["table_name"],
            "privilege": grant["privilege"],
            "scope": grant["scope"],
            "least_privilege_status": grant["least_privilege_status"],
            "row_level_security": grant["row_level_security"],
            "masking_required": grant["masking_required"],
            "status": grant["status"],
            "access_control_score": round(
                max(0.0, 0.40 * status_score(grant["least_privilege_status"]) + 0.30 * status_score(grant["status"]) + 0.20 * masking_fit + 0.10 * (1.0 - privilege_breadth)),
                3,
            ),
        })

    incident_rows = []
    for incident in incidents:
        incident_rows.append({
            "incident_id": incident["incident_id"],
            "table_name": incident["table_name"],
            "incident_type": incident["incident_type"],
            "affected_rows": incident["affected_rows"],
            "root_cause": incident["root_cause"],
            "severity": incident["severity"],
            "status": incident["status"],
            "incident_resolution_score": round(status_score(incident["status"]) * (1.0 - severity_weight(incident["severity"]) / 2.0), 3),
        })

    readiness = round(
        0.24 * mean([row["table_readiness_score"] for row in table_rows])
        + 0.18 * mean([row["constraint_score"] for row in constraint_rows])
        + 0.18 * mean([row["query_readiness_score"] for row in query_rows])
        + 0.14 * mean([row["transaction_score"] for row in transaction_rows])
        + 0.14 * mean([row["access_control_score"] for row in access_rows])
        + 0.12 * mean([row["incident_resolution_score"] for row in incident_rows]),
        3,
    )

    estate_summary = [{
        "evaluation_run_id": run_id,
        "table_count": len(schema),
        "constraint_count": len(constraints),
        "foreign_key_count": sum(1 for c in constraints if c["constraint_type"] == "foreign_key"),
        "query_workload_count": len(workloads),
        "index_count": len(indexes),
        "transaction_sample_count": len(transactions),
        "access_grant_count": len(access),
        "integrity_incident_count": len(incidents),
        "mean_table_readiness": round(mean([row["table_readiness_score"] for row in table_rows]), 3),
        "mean_constraint_score": round(mean([row["constraint_score"] for row in constraint_rows]), 3),
        "mean_query_readiness": round(mean([row["query_readiness_score"] for row in query_rows]), 3),
        "mean_transaction_score": round(mean([row["transaction_score"] for row in transaction_rows]), 3),
        "mean_access_control_score": round(mean([row["access_control_score"] for row in access_rows]), 3),
        "mean_incident_resolution_score": round(mean([row["incident_resolution_score"] for row in incident_rows]), 3),
        "relational_sql_readiness_score": readiness,
        "relational_sql_readiness_gap": round(1.0 - readiness, 3),
        "constraint_type_counts": json.dumps(Counter(c["constraint_type"] for c in constraints), sort_keys=True),
        "isolation_level_counts": json.dumps(Counter(t["isolation_level"] for t in transactions), sort_keys=True),
    }]

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_at,
        "article": "Relational Databases and SQL Systems",
        "workflow": "relational-sql-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "schema_inventory": {"path": str(schema_path), "sha256": sha256_file(schema_path), "rows": len(schema)},
            "constraint_inventory": {"path": str(constraints_path), "sha256": sha256_file(constraints_path), "rows": len(constraints)},
            "query_workload": {"path": str(workload_path), "sha256": sha256_file(workload_path), "rows": len(workloads)},
            "index_inventory": {"path": str(indexes_path), "sha256": sha256_file(indexes_path), "rows": len(indexes)},
            "normalization_checks": {"path": str(normalization_path), "sha256": sha256_file(normalization_path), "rows": len(normalization)},
            "transaction_log_sample": {"path": str(txn_path), "sha256": sha256_file(txn_path), "rows": len(transactions)},
            "access_controls": {"path": str(access_path), "sha256": sha256_file(access_path), "rows": len(access)},
            "integrity_incidents": {"path": str(incidents_path), "sha256": sha256_file(incidents_path), "rows": len(incidents)},
        },
    }

    write_csv(ROOT / "outputs" / "table_readiness_python.csv", table_rows)
    write_csv(ROOT / "outputs" / "constraint_scorecard_python.csv", constraint_rows)
    write_csv(ROOT / "outputs" / "query_workload_scorecard_python.csv", query_rows)
    write_csv(ROOT / "outputs" / "transaction_scorecard_python.csv", transaction_rows)
    write_csv(ROOT / "outputs" / "access_control_scorecard_python.csv", access_rows)
    write_csv(ROOT / "outputs" / "integrity_incident_scorecard_python.csv", incident_rows)
    write_csv(ROOT / "outputs" / "relational_sql_estate_summary_python.csv", estate_summary)
    (ROOT / "outputs" / "relational_sql_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Relational SQL scorecard complete")
    print(json.dumps({"tables": len(schema), "readiness": readiness}, indent=2))

if __name__ == "__main__":
    main()
