#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python data product scorecard..."
python3 python/product_scorecard.py

echo "Loading SQLite product governance example..."
python3 sql/run_sqlite_products.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R product summary..."
  Rscript r/product_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia readiness score..."
  julia julia/product_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go product contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust product inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C product registry fingerprint..."
  cc c/fnv_product_registry_fingerprint.c -o outputs/fnv_product_registry_fingerprint
  ./outputs/fnv_product_registry_fingerprint data/data_products.csv > outputs/fnv_product_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ lineage summary..."
  c++ -std=c++17 cpp/lineage_summary.cpp -o outputs/lineage_summary
  ./outputs/lineage_summary > outputs/lineage_summary_cpp.txt
  cat outputs/lineage_summary_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
