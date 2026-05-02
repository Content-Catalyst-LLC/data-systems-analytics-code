#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Profile the analytical mart.")
    parser.add_argument("--db", required=True)
    parser.add_argument("--output", default="outputs/data-profile.md")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    total = conn.execute("SELECT COUNT(*) AS n FROM mart_system_metrics").fetchone()["n"]
    warning = conn.execute("SELECT COUNT(*) AS n FROM mart_system_metrics WHERE quality_flag <> 'valid'").fetchone()["n"]
    systems = conn.execute("SELECT COUNT(DISTINCT system_id) AS n FROM mart_system_metrics").fetchone()["n"]
    metrics = conn.execute("SELECT COUNT(DISTINCT metric_name) AS n FROM mart_system_metrics").fetchone()["n"]
    summaries = conn.execute("SELECT * FROM v_metric_summary").fetchall()

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        f.write("# Data Profile\n\n")
        f.write(f"- Records: {total}\n")
        f.write(f"- Systems: {systems}\n")
        f.write(f"- Metrics: {metrics}\n")
        f.write(f"- Warning records: {warning}\n\n")
        f.write("## Metric Summary\n\n")
        f.write("| Domain | System | Metric | Unit | Records | Average | Min | Max |\n")
        f.write("|---|---|---|---|---:|---:|---:|---:|\n")
        for row in summaries:
            f.write(
                f"| {row['domain']} | {row['system_name']} | {row['metric_name']} | {row['unit']} | "
                f"{row['n_records']} | {row['avg_value']} | {row['min_value']} | {row['max_value']} |\n"
            )

    conn.close()
    print(f"Wrote profile to {out}")


if __name__ == "__main__":
    main()
