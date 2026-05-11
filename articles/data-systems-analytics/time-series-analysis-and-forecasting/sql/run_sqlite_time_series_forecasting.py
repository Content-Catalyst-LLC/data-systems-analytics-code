#!/usr/bin/env python3
import csv
import sqlite3
from pathlib import Path

ROOT = Path.cwd()
DB = ROOT / "outputs" / "time_series_forecasting.sqlite"

TABLES = {
    "monthly_demand": ROOT / "data" / "monthly_demand.csv",
    "forecast_model_registry": ROOT / "data" / "forecast_model_registry.csv",
    "backtest_windows": ROOT / "data" / "backtest_windows.csv",
    "diagnostic_checks": ROOT / "data" / "diagnostic_checks.csv",
    "forecast_horizons": ROOT / "data" / "forecast_horizons.csv",
}

DB.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
conn.executescript((ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))

for table, path in TABLES.items():
    conn.execute(f"DELETE FROM {table}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        placeholders = ",".join([f":{col}" for col in columns])
        column_sql = ",".join(columns)
        conn.executemany(
            f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})",
            reader,
        )

conn.commit()

print(f"SQLite time-series forecasting database written to {DB}")
print("Diagnostic checks requiring review:")
for row in conn.execute("""
    SELECT series_id, check_type, status, severity, remediation
    FROM diagnostic_checks
    WHERE status <> 'pass'
    ORDER BY severity DESC, check_type
"""):
    print(row)

conn.close()
