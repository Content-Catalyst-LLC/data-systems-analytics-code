#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
from typing import Iterable

REQUIRED_OBSERVATION_FIELDS = {
    "observation_id",
    "system_id",
    "observed_at",
    "metric_name",
    "metric_value",
    "unit",
    "source_system",
}


def validate_headers(path: Path, required: set[str]) -> None:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path} is missing required fields: {sorted(missing)}")


def load_csv(conn: sqlite3.Connection, table: str, path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return 0
    cols = list(rows[0].keys())
    placeholders = ",".join(["?"] * len(cols))
    col_sql = ",".join(cols)
    values = [[row[col] for col in cols] for row in rows]
    conn.executemany(f"INSERT OR REPLACE INTO {table} ({col_sql}) VALUES ({placeholders})", values)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local-first data systems ETL workflow.")
    parser.add_argument("--db", default="data_systems.db")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    db_path = Path(args.db)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    observations_path = Path("data/raw/observations.csv")
    entities_path = Path("data/raw/entities.csv")
    validate_headers(observations_path, REQUIRED_OBSERVATION_FIELDS)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")

    # Load schema and views if they have not already been applied.
    for sql_file in ["sql/schema.sql", "sql/views.sql"]:
        conn.executescript(Path(sql_file).read_text(encoding="utf-8"))

    n_entities = load_csv(conn, "dim_systems", entities_path)
    n_observations = load_csv(conn, "stg_observations", observations_path)
    conn.commit()

    conn.executescript(Path("sql/data_quality_checks.sql").read_text(encoding="utf-8"))
    quality_rows = conn.execute("SELECT check_name, check_status, failed_records FROM data_quality_results").fetchall()

    summary_rows = conn.execute("SELECT * FROM v_metric_summary").fetchall()
    summary_cols = [desc[0] for desc in conn.execute("SELECT * FROM v_metric_summary").description]

    output_csv = output_dir / "metric-summary.csv"
    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(summary_cols)
        writer.writerows(summary_rows)

    output_md = output_dir / "etl-run-summary.md"
    with output_md.open("w", encoding="utf-8") as f:
        f.write("# ETL Run Summary\n\n")
        f.write(f"- Database: `{db_path}`\n")
        f.write(f"- Entities loaded: {n_entities}\n")
        f.write(f"- Observations loaded: {n_observations}\n\n")
        f.write("## Data Quality Checks\n\n")
        for check_name, check_status, failed_records in quality_rows:
            f.write(f"- {check_name}: **{check_status}** ({failed_records} failed records)\n")
        f.write(f"\nMetric summary written to `{output_csv}`.\n")

    conn.close()
    print(f"Wrote {output_md} and {output_csv}")


if __name__ == "__main__":
    main()
