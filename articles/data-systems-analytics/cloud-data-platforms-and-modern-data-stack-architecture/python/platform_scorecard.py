#!/usr/bin/env python3
"""
Vendor-neutral cloud data platform scorecard.

The script reads architecture inventory files and produces:
- layer coverage
- governance coverage
- observability coverage
- pipeline dependency inventory
- cost summary
- platform manifest
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


def main() -> None:
    components_path = ROOT / "data" / "stack_components.csv"
    pipelines_path = ROOT / "data" / "pipeline_catalog.csv"
    policies_path = ROOT / "data" / "access_policies.csv"
    costs_path = ROOT / "data" / "cost_events.csv"

    components = read_csv(components_path)
    pipelines = read_csv(pipelines_path)
    policies = read_csv(policies_path)
    costs = read_csv(costs_path)

    required_layers = {
        "source", "ingestion", "storage", "transformation", "orchestration",
        "metadata", "lineage", "semantic", "serving", "consumption"
    }

    present_layers = {row["layer"] for row in components}
    missing_layers = sorted(required_layers - present_layers)

    layer_counts = Counter(row["layer"] for row in components)
    layer_rows = [
        {
            "layer": layer,
            "component_count": layer_counts[layer],
            "coverage_status": "present" if layer_counts[layer] > 0 else "missing",
        }
        for layer in sorted(required_layers | present_layers)
    ]

    governed = sum(1 for row in components if row["governance_control"].strip())
    observed = sum(1 for row in components if row["observability_control"].strip())

    cost_by_category: dict[str, float] = defaultdict(float)
    for row in costs:
        cost_by_category[row["service_category"]] += float(row["estimated_cost"])

    cost_rows = [
        {"service_category": key, "estimated_cost": round(value, 2)}
        for key, value in sorted(cost_by_category.items())
    ]

    pipeline_rows = []
    for row in pipelines:
        pipeline_rows.append(
            {
                "pipeline_id": row["pipeline_id"],
                "edge": f"{row['source_layer']} -> {row['target_layer']}",
                "latency_pattern": row["latency_pattern"],
                "owner": row["owner"],
                "quality_gate": row["quality_gate"],
            }
        )

    run_id = str(uuid.uuid4())
    manifest = {
        "run_id": run_id,
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Cloud Data Platforms and Modern Data Stack Architecture",
        "workflow": "vendor-neutral-platform-scorecard",
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "inputs": {
            "stack_components": {
                "path": str(components_path),
                "sha256": sha256_file(components_path),
                "rows": len(components),
            },
            "pipeline_catalog": {
                "path": str(pipelines_path),
                "sha256": sha256_file(pipelines_path),
                "rows": len(pipelines),
            },
            "access_policies": {
                "path": str(policies_path),
                "sha256": sha256_file(policies_path),
                "rows": len(policies),
            },
            "cost_events": {
                "path": str(costs_path),
                "sha256": sha256_file(costs_path),
                "rows": len(costs),
            },
        },
        "architecture_scorecard": {
            "required_layer_count": len(required_layers),
            "present_layer_count": len(required_layers - set(missing_layers)),
            "missing_layers": missing_layers,
            "governance_control_coverage": round(governed / len(components), 3),
            "observability_control_coverage": round(observed / len(components), 3),
            "pipeline_count": len(pipelines),
            "policy_count": len(policies),
            "estimated_total_cost": round(sum(float(row["estimated_cost"]) for row in costs), 2),
        },
        "outputs": {
            "layer_coverage": "outputs/layer_coverage_python.csv",
            "pipeline_edges": "outputs/pipeline_edges_python.csv",
            "cost_summary": "outputs/cost_summary_python.csv",
            "manifest": "outputs/platform_manifest_python.json",
        },
    }

    write_csv(ROOT / "outputs" / "layer_coverage_python.csv", layer_rows)
    write_csv(ROOT / "outputs" / "pipeline_edges_python.csv", pipeline_rows)
    write_csv(ROOT / "outputs" / "cost_summary_python.csv", cost_rows)
    (ROOT / "outputs").mkdir(exist_ok=True)
    (ROOT / "outputs" / "platform_manifest_python.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print("Cloud platform scorecard complete")
    print(json.dumps(manifest["architecture_scorecard"], indent=2))


if __name__ == "__main__":
    main()
