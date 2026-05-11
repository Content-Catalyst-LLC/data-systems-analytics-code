#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python interoperability scorecard..."
python3 python/interoperability_scorecard.py

echo "Loading SQLite interoperability governance example..."
python3 sql/run_sqlite_interoperability.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R integration quality summary..."
  Rscript r/integration_quality_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia mapping readiness score..."
  julia julia/mapping_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go interoperability contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust interoperability inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C mapping registry fingerprint..."
  cc c/fnv_mapping_registry_fingerprint.c -o outputs/fnv_mapping_registry_fingerprint
  ./outputs/fnv_mapping_registry_fingerprint data/schema_mappings.csv > outputs/fnv_mapping_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ lineage adjacency..."
  c++ -std=c++17 cpp/lineage_adjacency.cpp -o outputs/lineage_adjacency
  ./outputs/lineage_adjacency > outputs/lineage_adjacency_cpp.txt
  cat outputs/lineage_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
