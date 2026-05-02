#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate simple analytical features from system metrics.")
    parser.add_argument("--db", required=True)
    parser.add_argument("--output", default="data/processed/system_features.csv")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        """
        SELECT
            system_id,
            system_name,
            domain,
            criticality,
            COUNT(*) AS n_observations,
            AVG(metric_value) AS avg_metric_value,
            MAX(CASE WHEN quality_flag <> 'valid' THEN 1 ELSE 0 END) AS has_warning
        FROM mart_system_metrics
        GROUP BY system_id, system_name, domain, criticality
        ORDER BY domain, system_id;
        """
    ).fetchall()
    conn.close()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        if rows:
            writer.writeheader()
            writer.writerows(dict(row) for row in rows)

    print(f"Wrote features to {out}")


if __name__ == "__main__":
    main()
