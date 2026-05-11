#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python data quality scorecard..."
python3 python/data_quality_scorecard.py

echo "Loading SQLite data quality example..."
python3 sql/run_sqlite_data_quality.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R data quality summary..."
  Rscript r/data_quality_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia data quality readiness score..."
  julia julia/data_quality_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go data quality raw-record validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust data quality inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C data quality fingerprint..."
  cc c/fnv_data_quality_fingerprint.c -o outputs/fnv_data_quality_fingerprint
  ./outputs/fnv_data_quality_fingerprint data/raw_customer_records.csv > outputs/fnv_data_quality_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ quality rule adjacency..."
  c++ -std=c++17 cpp/quality_rule_adjacency.cpp -o outputs/quality_rule_adjacency
  ./outputs/quality_rule_adjacency > outputs/quality_rule_adjacency_cpp.txt
  cat outputs/quality_rule_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto data quality template..."
  quarto render quarto/data-quality-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
