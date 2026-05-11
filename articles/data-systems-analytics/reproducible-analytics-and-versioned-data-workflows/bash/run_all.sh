#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Running portable Python workflow..."
python3 python/reproducible_workflow.py --group-by system

echo "Loading SQLite example..."
python3 sql/run_sqlite_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/reproducible_workflow.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/reproducible_workflow.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C fingerprint example..."
  cc c/fnv_fingerprint.c -o outputs/fnv_fingerprint
  ./outputs/fnv_fingerprint data/sample_events.csv > outputs/fnv_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ summary example..."
  c++ -std=c++17 cpp/reproducible_summary.cpp -o outputs/reproducible_summary_cpp
  ./outputs/reproducible_summary_cpp
else
  echo "Skipping C++ example: c++ not found"
fi

echo "Done. Review generated files in outputs/."
