#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python quality observability scorecard..."
python3 python/quality_observability_scorecard.py

echo "Loading SQLite quality observability governance example..."
python3 sql/run_sqlite_quality_observability.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R quality observability summary..."
  Rscript r/quality_observability_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia dataset reliability score..."
  julia julia/dataset_reliability_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go quality check contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust quality incident inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C quality check fingerprint..."
  cc c/fnv_quality_check_fingerprint.c -o outputs/fnv_quality_check_fingerprint
  ./outputs/fnv_quality_check_fingerprint data/quality_checks.csv > outputs/fnv_quality_check_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ lineage impact adjacency..."
  c++ -std=c++17 cpp/lineage_impact_adjacency.cpp -o outputs/lineage_impact_adjacency
  ./outputs/lineage_impact_adjacency > outputs/lineage_impact_adjacency_cpp.txt
  cat outputs/lineage_impact_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
