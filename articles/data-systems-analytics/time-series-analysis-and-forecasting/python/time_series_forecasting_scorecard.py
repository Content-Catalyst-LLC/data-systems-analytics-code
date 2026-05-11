#!/usr/bin/env python3
"""
Python Workflow: Time Series Forecasting Scorecard

This workflow evaluates temporal structure, rolling-origin forecast errors,
prediction interval coverage, diagnostics, and forecast governance using only
the Python standard library.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import statistics
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

def status_score(value: str) -> float:
    return {
        "approved": 1.0,
        "pass": 1.0,
        "in_review": 0.7,
        "watch": 0.55,
        "planned": 0.45,
        "needs_revision": 0.15,
        "fail": 0.0,
    }.get(value, 0.5)

def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def acf(values: list[float], lag: int) -> float:
    if lag <= 0 or lag >= len(values):
        return 0.0
    x = values[lag:]
    y = values[:-lag]
    mx = mean(x)
    my = mean(y)
    numerator = sum((a - mx) * (b - my) for a, b in zip(x, y))
    denominator = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    return numerator / denominator if denominator else 0.0

def rolling_seasonal_naive(values: list[float], season: int = 12, min_train: int = 18) -> list[dict[str, object]]:
    rows = []
    for idx in range(min_train, len(values)):
        if idx - season >= 0:
            forecast = values[idx - season]
        else:
            forecast = values[idx - 1]
        actual = values[idx]
        rows.append({
            "origin_index": idx - 1,
            "target_index": idx,
            "actual": actual,
            "forecast": forecast,
            "error": actual - forecast,
            "absolute_error": abs(actual - forecast),
            "squared_error": (actual - forecast) ** 2,
        })
    return rows

def moving_average_forecast(values: list[float], window: int = 3, min_train: int = 18) -> list[dict[str, object]]:
    rows = []
    for idx in range(min_train, len(values)):
        train = values[:idx]
        forecast = mean(train[-window:])
        actual = values[idx]
        rows.append({
            "origin_index": idx - 1,
            "target_index": idx,
            "actual": actual,
            "forecast": round(forecast, 4),
            "error": round(actual - forecast, 4),
            "absolute_error": round(abs(actual - forecast), 4),
            "squared_error": round((actual - forecast) ** 2, 4),
        })
    return rows

def error_summary(rows: list[dict[str, object]]) -> dict[str, float]:
    errors = [float(r["error"]) for r in rows]
    abs_errors = [abs(e) for e in errors]
    sq_errors = [e ** 2 for e in errors]
    actuals = [float(r["actual"]) for r in rows]
    ape = [abs(e) / max(abs(a), 1e-9) for e, a in zip(errors, actuals)]
    return {
        "mae": mean(abs_errors),
        "rmse": math.sqrt(mean(sq_errors)),
        "bias": mean(errors),
        "mape": mean(ape),
    }

def main() -> None:
    observations_path = ROOT / "data" / "monthly_demand.csv"
    registry_path = ROOT / "data" / "forecast_model_registry.csv"
    backtest_path = ROOT / "data" / "backtest_windows.csv"
    checks_path = ROOT / "data" / "diagnostic_checks.csv"
    horizons_path = ROOT / "data" / "forecast_horizons.csv"

    observations = read_csv(observations_path)
    registry = read_csv(registry_path)
    backtests = read_csv(backtest_path)
    checks = read_csv(checks_path)
    horizons = read_csv(horizons_path)

    values = [float(row["value"]) for row in observations]
    dates = [row["date"] for row in observations]

    diagnostic_rows = []
    for lag in [1, 2, 3, 6, 12]:
        diagnostic_rows.append({
            "series_id": "demand",
            "diagnostic": "autocorrelation",
            "lag": lag,
            "value": round(acf(values, lag), 4),
        })

    year_means = defaultdict(list)
    for row in observations:
        year_means[row["date"][:4]].append(float(row["value"]))
    for year, vals in sorted(year_means.items()):
        diagnostic_rows.append({
            "series_id": "demand",
            "diagnostic": "year_mean",
            "lag": "",
            "value": round(mean(vals), 4),
        })

    seasonal_rows = rolling_seasonal_naive(values)
    ma_rows = moving_average_forecast(values)

    for row in seasonal_rows:
        row["model_id"] = "generated_seasonal_naive"
        row["origin_date"] = dates[int(row["origin_index"])]
        row["target_date"] = dates[int(row["target_index"])]

    for row in ma_rows:
        row["model_id"] = "generated_moving_average"
        row["origin_date"] = dates[int(row["origin_index"])]
        row["target_date"] = dates[int(row["target_index"])]

    generated_summary = []
    for model_id, rows in [
        ("generated_seasonal_naive", seasonal_rows),
        ("generated_moving_average", ma_rows),
    ]:
        summary = error_summary(rows)
        generated_summary.append({
            "model_id": model_id,
            **{k: round(v, 4) for k, v in summary.items()},
            "backtest_points": len(rows),
        })

    backtest_by_model = defaultdict(list)
    for row in backtests:
        backtest_by_model[row["model_id"]].append(row)

    model_scorecard = []
    for model in registry:
        model_id = model["model_id"]
        rows = backtest_by_model.get(model_id, [])
        if rows:
            errors = [float(r["actual"]) - float(r["forecast"]) for r in rows]
            abs_errors = [abs(e) for e in errors]
            sq_errors = [e ** 2 for e in errors]
            interval_hits = [
                1 if float(r["lower_80"]) <= float(r["actual"]) <= float(r["upper_80"]) else 0
                for r in rows
            ]
            mae = mean(abs_errors)
            rmse = math.sqrt(mean(sq_errors))
            interval_coverage = mean(interval_hits)
            evidence_score = max(0.0, min(1.0, 1.0 - mae / 50.0))
        else:
            mae = rmse = interval_coverage = 0.0
            evidence_score = 0.35

        validation_score = 1.0 if model["validation_design"] == "rolling_origin" else 0.35
        horizon_score = 1.0 if int(model["horizon"]) >= 3 else 0.6
        status = status_score(model["status"])

        readiness = round(
            0.30 * validation_score
            + 0.25 * evidence_score
            + 0.15 * interval_coverage
            + 0.15 * horizon_score
            + 0.15 * status,
            3,
        )

        model_scorecard.append({
            "model_id": model_id,
            "model_family": model["model_family"],
            "validation_design": model["validation_design"],
            "status": model["status"],
            "mae": round(mae, 4),
            "rmse": round(rmse, 4),
            "interval_coverage_80": round(interval_coverage, 4),
            "forecast_readiness_score": readiness,
            "forecast_readiness_gap": round(1.0 - readiness, 3),
        })

    horizon_summary = []
    by_horizon = defaultdict(list)
    for row in horizons:
        width_80 = float(row["upper_80"]) - float(row["lower_80"])
        width_95 = float(row["upper_95"]) - float(row["lower_95"])
        by_horizon[(row["model_id"], row["horizon"])].append((width_80, width_95))

    for (model_id, horizon), widths in sorted(by_horizon.items()):
        horizon_summary.append({
            "model_id": model_id,
            "horizon": horizon,
            "mean_width_80": round(mean([w[0] for w in widths]), 4),
            "mean_width_95": round(mean([w[1] for w in widths]), 4),
        })

    check_summary = [
        {"check_type": check, "count": count}
        for check, count in sorted(Counter(row["status"] for row in checks).items())
    ]

    manifest = {
        "run_id": str(uuid.uuid4()),
        "run_started_at_utc": datetime.now(timezone.utc).isoformat(),
        "article": "Time Series Analysis and Forecasting",
        "workflow": "time-series-forecasting-scorecard",
        "runtime": {"python": sys.version, "platform": platform.platform()},
        "inputs": {
            "monthly_demand": {"path": str(observations_path), "sha256": sha256_file(observations_path), "rows": len(observations)},
            "forecast_model_registry": {"path": str(registry_path), "sha256": sha256_file(registry_path), "rows": len(registry)},
            "backtest_windows": {"path": str(backtest_path), "sha256": sha256_file(backtest_path), "rows": len(backtests)},
            "diagnostic_checks": {"path": str(checks_path), "sha256": sha256_file(checks_path), "rows": len(checks)},
            "forecast_horizons": {"path": str(horizons_path), "sha256": sha256_file(horizons_path), "rows": len(horizons)},
        },
    }

    write_csv(ROOT / "outputs" / "time_series_diagnostics_python.csv", diagnostic_rows)
    write_csv(ROOT / "outputs" / "generated_backtest_errors_python.csv", seasonal_rows + ma_rows)
    write_csv(ROOT / "outputs" / "generated_backtest_summary_python.csv", generated_summary)
    write_csv(ROOT / "outputs" / "forecast_model_scorecard_python.csv", model_scorecard)
    write_csv(ROOT / "outputs" / "forecast_horizon_interval_summary_python.csv", horizon_summary)
    write_csv(ROOT / "outputs" / "diagnostic_check_status_summary_python.csv", check_summary)
    (ROOT / "outputs" / "time_series_forecasting_manifest_python.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Time-series forecasting scorecard complete")
    print(json.dumps({"observations": len(observations), "models": len(registry), "backtests": len(backtests)}, indent=2))

if __name__ == "__main__":
    main()
