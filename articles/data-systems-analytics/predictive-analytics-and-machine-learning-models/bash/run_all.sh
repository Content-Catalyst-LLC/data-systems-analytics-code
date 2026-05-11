#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python predictive analytics scorecard..."
python3 python/predictive_model_scorecard.py

echo "Loading SQLite predictive analytics example..."
python3 sql/run_sqlite_predictive_analytics.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R predictive analytics summary..."
  Rscript r/predictive_analytics_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia predictive readiness score..."
  julia julia/predictive_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go predictive model registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust predictive model inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C prediction dataset fingerprint..."
  cc c/fnv_prediction_dataset_fingerprint.c -o outputs/fnv_prediction_dataset_fingerprint
  ./outputs/fnv_prediction_dataset_fingerprint data/classification_predictions.csv > outputs/fnv_prediction_dataset_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ model evidence adjacency..."
  c++ -std=c++17 cpp/model_evidence_adjacency.cpp -o outputs/model_evidence_adjacency
  ./outputs/model_evidence_adjacency > outputs/model_evidence_adjacency_cpp.txt
  cat outputs/model_evidence_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto predictive analytics template..."
  quarto render quarto/predictive-analytics-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
