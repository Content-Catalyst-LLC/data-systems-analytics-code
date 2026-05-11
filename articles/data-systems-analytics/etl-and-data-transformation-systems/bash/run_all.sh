#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python ETL transformation scorecard..."
python3 python/etl_transformation_scorecard.py

echo "Loading SQLite ETL transformation example..."
python3 sql/run_sqlite_etl_transformation.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R ETL transformation summary..."
  Rscript r/etl_transformation_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia ETL readiness score..."
  julia julia/etl_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go extract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust extract inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C extract fingerprint..."
  cc c/fnv_extract_fingerprint.c -o outputs/fnv_extract_fingerprint
  ./outputs/fnv_extract_fingerprint data/raw_customer_extract.csv > outputs/fnv_extract_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ transformation lineage adjacency..."
  c++ -std=c++17 cpp/transformation_lineage_adjacency.cpp -o outputs/transformation_lineage_adjacency
  ./outputs/transformation_lineage_adjacency > outputs/transformation_lineage_adjacency_cpp.txt
  cat outputs/transformation_lineage_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto ETL transformation template..."
  quarto render quarto/etl-transformation-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
