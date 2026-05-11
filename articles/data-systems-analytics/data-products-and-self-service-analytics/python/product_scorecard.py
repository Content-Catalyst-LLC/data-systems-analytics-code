#!/usr/bin/env python3
"""
Data product and self-service analytics scorecard.

This script reads a small product registry, semantic metric catalog, access-event
table, quality-check inventory, and lineage map. It generates a product-readiness
scorecard, usage summary, quality summary, and manifest.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
import uuid
from collections import defaultdict
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


def main() -> None:
    products_path = ROOT / "data" / "data_products.csv"
    metrics_path = ROOT / "data" / "semantic_metrics.csv"
    access_path = ROOT / "data" / "access_events.csv"
    quality_path = ROOT / "data" / "quality_checks.csv"
    lineage_path = ROOT / "data" / "product_lineage.csv"

    products = read_csv(products_path)
    metrics = read_csv(metrics_path)
    access = read_csv(access_path)
    quality = read_csv(quality_path)
    lineage = read_csv(lineage_path)

    certified_metrics_by_product: dict[str, int] = defaultdict(int)
    reviewed_metrics_by_product: dict[str, int] = defaultdict(int)
    for row in metrics:
        if row["certification_status"] == "certified":
            certified_metrics_by_product[row["product_id"]] += 1
        elif row["certification_status"] == "reviewed":
            reviewed_metrics_by_product[row["product_id"]] += 1

    quality_status_by_product: dict[str, list[str]] = defaultdict(list)
    for row in quality:
        quality_status_by_product[row["product_id"]].append(row["last_status"])

    usage_by_product: dict[str, dict[str, int]] = defaultdict(lambda: {
        "dashboard_views": 0,
        "notebook_sessions": 0,
        "api_calls": 0,
        "ad_hoc_queries": 0,
    })
    for row in access:
        bucket = usage_by_product[row["product_id"]]
        for field in bucket:
            bucket[field] += int(row[field])

    lineage_by_product = {row["product_id"]: row for row in lineage}

    scorecard_rows: list[dict[str, object]] = []
    for product in products:
        product_id = product["product_id"]
        status_list = quality_status_by_product.get(product_id, [])
        passed_checks = sum(1 for status in status_list if status == "pass")
        total_checks = len(status_list)
        quality_pass_rate = passed_checks / total_checks if total_checks else 0.0

        semantic_weight = {
            "certified": 1.0,
            "reviewed": 0.7,
            "uncertified": 0.2,
        }.get(product["semantic_status"], 0.0)

        lifecycle_weight = {
            "active": 1.0,
            "beta": 0.7,
            "deprecated": 0.2,
            "retired": 0.0,
        }.get(product["lifecycle_status"], 0.5)

        lineage_present = 1.0 if product_id in lineage_by_product else 0.0
        certified_metric_count = certified_metrics_by_product[product_id]
        metric_weight = min(certified_metric_count / 2, 1.0)

        readiness_score = round(
            0.30 * float(product["quality_score"])
            + 0.20 * quality_pass_rate
            + 0.20 * semantic_weight
            + 0.15 * lifecycle_weight
            + 0.10 * lineage_present
            + 0.05 * metric_weight,
            3,
        )

        usage = usage_by_product[product_id]
        total_usage = sum(usage.values())

        scorecard_rows.append({
            "product_id": product_id,
            "domain": product["domain"],
            "product_name": product["product_name"],
            "owner": product["owner"],
            "semantic_status": product["semantic_status"],
            "lifecycle_status": product["lifecycle_status"],
            "quality_pass_rate": round(quality_pass_rate, 3),
            "certified_metric_count": certified_metric_count,
            "total_usage_events": total_usage,
            "readiness_score": readiness_score,
        })

    usage_rows = [
        {"product_id": product_id, **values, "total_usage": sum(values.values())}
        for product_id, values in sorted(usage_by_product.items())
    ]

    quality_rows = []
    for product_id, statuses in sorted(quality_status_by_product.items()):
        quality_rows.append({
            "product_id": product_id,
            "checks": len(statuses),
            "pass": statuses.count("pass"),
            "warn": statuses.count("warn"),
            "fail": statuses.count("fail"),
        })

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Data Products and Self-Service Analytics",
        "workflow": "data-product-scorecard",
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "inputs": {
            "data_products": {"path": str(products_path), "sha256": sha256_file(products_path), "rows": len(products)},
            "semantic_metrics": {"path": str(metrics_path), "sha256": sha256_file(metrics_path), "rows": len(metrics)},
            "access_events": {"path": str(access_path), "sha256": sha256_file(access_path), "rows": len(access)},
            "quality_checks": {"path": str(quality_path), "sha256": sha256_file(quality_path), "rows": len(quality)},
            "product_lineage": {"path": str(lineage_path), "sha256": sha256_file(lineage_path), "rows": len(lineage)},
        },
        "outputs": {
            "scorecard": "outputs/product_scorecard_python.csv",
            "usage_summary": "outputs/product_usage_summary_python.csv",
            "quality_summary": "outputs/product_quality_summary_python.csv",
            "manifest": "outputs/product_platform_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "product_scorecard_python.csv", scorecard_rows)
    write_csv(ROOT / "outputs" / "product_usage_summary_python.csv", usage_rows)
    write_csv(ROOT / "outputs" / "product_quality_summary_python.csv", quality_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "product_platform_manifest_python.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Data product scorecard complete")
    print(json.dumps({
        "products": len(products),
        "metrics": len(metrics),
        "quality_checks": len(quality),
        "lineage_edges": len(lineage),
    }, indent=2))


if __name__ == "__main__":
    main()
