#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python warehouse/lake scorecard..."
python3 python/warehouse_lake_scorecard.py

echo "Loading SQLite warehouse/lake example..."
python3 sql/run_sqlite_warehouse_lake.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R warehouse/lake summary..."
  Rscript r/warehouse_lake_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia warehouse/lake readiness score..."
  julia julia/warehouse_lake_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go data asset validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust warehouse/lake inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C asset fingerprint..."
  cc c/fnv_warehouse_lake_fingerprint.c -o outputs/fnv_warehouse_lake_fingerprint
  ./outputs/fnv_warehouse_lake_fingerprint data/data_assets.csv > outputs/fnv_warehouse_lake_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ dimensional model adjacency..."
  c++ -std=c++17 cpp/star_schema_adjacency.cpp -o outputs/star_schema_adjacency
  ./outputs/star_schema_adjacency > outputs/star_schema_adjacency_cpp.txt
  cat outputs/star_schema_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto warehouse/lake template..."
  quarto render quarto/warehouse-lake-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
