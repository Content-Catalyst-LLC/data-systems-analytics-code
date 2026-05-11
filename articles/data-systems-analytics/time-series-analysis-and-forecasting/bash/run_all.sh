#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python time-series forecasting scorecard..."
python3 python/time_series_forecasting_scorecard.py

echo "Loading SQLite time-series forecasting example..."
python3 sql/run_sqlite_time_series_forecasting.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R time-series forecasting summary..."
  Rscript r/time_series_forecasting_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia forecast readiness score..."
  julia julia/forecast_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go forecast model registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust forecast inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C time-series fingerprint..."
  cc c/fnv_time_series_fingerprint.c -o outputs/fnv_time_series_fingerprint
  ./outputs/fnv_time_series_fingerprint data/monthly_demand.csv > outputs/fnv_time_series_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ forecast horizon adjacency..."
  c++ -std=c++17 cpp/forecast_horizon_adjacency.cpp -o outputs/forecast_horizon_adjacency
  ./outputs/forecast_horizon_adjacency > outputs/forecast_horizon_adjacency_cpp.txt
  cat outputs/forecast_horizon_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto time-series template..."
  quarto render quarto/time-series-forecasting-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
