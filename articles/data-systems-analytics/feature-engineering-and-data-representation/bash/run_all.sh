#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python feature engineering scorecard..."
python3 python/feature_engineering_scorecard.py

echo "Loading SQLite feature engineering example..."
python3 sql/run_sqlite_feature_engineering.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R feature engineering summary..."
  Rscript r/feature_engineering_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia representation readiness score..."
  julia julia/representation_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go feature registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust feature registry inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C feature registry fingerprint..."
  cc c/fnv_feature_registry_fingerprint.c -o outputs/fnv_feature_registry_fingerprint
  ./outputs/fnv_feature_registry_fingerprint data/feature_registry.csv > outputs/fnv_feature_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ feature-source adjacency..."
  c++ -std=c++17 cpp/feature_source_adjacency.cpp -o outputs/feature_source_adjacency
  ./outputs/feature_source_adjacency > outputs/feature_source_adjacency_cpp.txt
  cat outputs/feature_source_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto feature engineering template..."
  quarto render quarto/feature-engineering-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
