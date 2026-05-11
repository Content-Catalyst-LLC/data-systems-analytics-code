#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python dashboard/storytelling integrity scorecard..."
python3 python/dashboard_storytelling_scorecard.py

echo "Loading SQLite dashboard/storytelling governance example..."
python3 sql/run_sqlite_dashboard_storytelling.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R dashboard/storytelling summary..."
  Rscript r/dashboard_storytelling_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia dashboard readiness score..."
  julia julia/dashboard_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go dashboard registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust dashboard inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C dashboard registry fingerprint..."
  cc c/fnv_dashboard_registry_fingerprint.c -o outputs/fnv_dashboard_registry_fingerprint
  ./outputs/fnv_dashboard_registry_fingerprint data/dashboard_inventory.csv > outputs/fnv_dashboard_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ story evidence adjacency..."
  c++ -std=c++17 cpp/story_evidence_adjacency.cpp -o outputs/story_evidence_adjacency
  ./outputs/story_evidence_adjacency > outputs/story_evidence_adjacency_cpp.txt
  cat outputs/story_evidence_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto dashboard story template..."
  quarto render quarto/dashboard-story-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
