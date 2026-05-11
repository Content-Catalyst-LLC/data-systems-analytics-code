#!/usr/bin/env python3
"""
Portable reproducible analytics workflow.

This script uses only the Python standard library so that the example is easy
to run in constrained environments. It demonstrates the core pattern:
fingerprint inputs, capture parameters, produce outputs, fingerprint outputs,
and write a manifest that connects them.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "unavailable"


def read_events(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def summarize(events: list[dict[str, str]], group_by: str) -> list[dict[str, str]]:
    totals: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)

    for row in events:
        key = row[group_by]
        totals[key] += int(row["value"])
        counts[key] += 1

    result: list[dict[str, str]] = []
    for key in sorted(totals):
        result.append(
            {
                group_by: key,
                "records": str(counts[key]),
                "total_value": str(totals[key]),
                "average_value": f"{totals[key] / counts[key]:.2f}",
            }
        )
    return result


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/sample_events.csv")
    parser.add_argument("--output", default="outputs/run_summary_python.csv")
    parser.add_argument("--manifest", default="outputs/run_manifest_python.json")
    parser.add_argument("--group-by", default="system", choices=["region", "system", "event_type"])
    parser.add_argument("--workflow-version", default="0.1.0")
    args = parser.parse_args()

    repo_root = Path.cwd()
    input_path = repo_root / args.input
    output_path = repo_root / args.output
    manifest_path = repo_root / args.manifest

    run_id = str(uuid.uuid4())
    run_started_at = datetime.now(timezone.utc).isoformat()

    snapshot_dir = repo_root / "data" / "snapshots" / run_id
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / input_path.name
    shutil.copy2(input_path, snapshot_path)

    events = read_events(snapshot_path)
    summary = summarize(events, args.group_by)
    write_csv(output_path, summary)

    manifest = {
        "run_id": run_id,
        "run_started_at_utc": run_started_at,
        "workflow_name": "reproducible-analytics-and-versioned-data-workflows",
        "workflow_version": args.workflow_version,
        "git_commit": git_commit(),
        "parameters": {
            "group_by": args.group_by,
        },
        "environment": {
            "python_version": sys.version,
            "platform": platform.platform(),
            "executable": sys.executable,
            "working_directory": str(repo_root),
        },
        "inputs": {
            "source_path": str(input_path),
            "snapshot_path": str(snapshot_path),
            "sha256": sha256_file(snapshot_path),
            "rows": len(events),
        },
        "outputs": {
            "summary_path": str(output_path),
            "summary_sha256": sha256_file(output_path),
            "manifest_path": str(manifest_path),
        },
        "lineage": [
            {
                "from": str(snapshot_path),
                "to": str(output_path),
                "transformation": "grouped aggregation",
                "group_by": args.group_by,
            }
        ],
    }

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Run complete: {run_id}")
    print(f"Wrote {output_path}")
    print(f"Wrote {manifest_path}")


if __name__ == "__main__":
    main()
