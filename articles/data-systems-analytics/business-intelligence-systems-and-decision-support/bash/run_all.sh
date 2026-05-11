#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python BI decision-support scorecard..."
python3 python/decision_support_scorecard.py

echo "Loading SQLite BI governance example..."
python3 sql/run_sqlite_bi.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R BI usage and decision review summary..."
  Rscript r/bi_usage_decision_review.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia BI readiness score..."
  julia julia/bi_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go BI dashboard contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust BI metric inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C BI registry fingerprint..."
  cc c/fnv_bi_registry_fingerprint.c -o outputs/fnv_bi_registry_fingerprint
  ./outputs/fnv_bi_registry_fingerprint data/dashboard_inventory.csv > outputs/fnv_bi_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ alert pathway summary..."
  c++ -std=c++17 cpp/alert_pathway_summary.cpp -o outputs/alert_pathway_summary
  ./outputs/alert_pathway_summary > outputs/alert_pathway_summary_cpp.txt
  cat outputs/alert_pathway_summary_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
