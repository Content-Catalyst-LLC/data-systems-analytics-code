#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python visualization integrity scorecard..."
python3 python/visualization_integrity_scorecard.py

echo "Loading SQLite visualization integrity example..."
python3 sql/run_sqlite_visualization_integrity.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R visualization communication summary..."
  Rscript r/visualization_communication_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia visualization readiness score..."
  julia julia/visualization_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go visualization registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust visualization inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C visualization registry fingerprint..."
  cc c/fnv_visualization_registry_fingerprint.c -o outputs/fnv_visualization_registry_fingerprint
  ./outputs/fnv_visualization_registry_fingerprint data/visualization_inventory.csv > outputs/fnv_visualization_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ chart evidence adjacency..."
  c++ -std=c++17 cpp/chart_evidence_adjacency.cpp -o outputs/chart_evidence_adjacency
  ./outputs/chart_evidence_adjacency > outputs/chart_evidence_adjacency_cpp.txt
  cat outputs/chart_evidence_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto visualization communication template..."
  quarto render quarto/visualization-communication-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
