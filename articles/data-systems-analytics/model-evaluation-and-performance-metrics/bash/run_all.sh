#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python model evaluation scorecard..."
python3 python/model_evaluation_scorecard.py

echo "Loading SQLite model evaluation example..."
python3 sql/run_sqlite_model_evaluation.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R model evaluation summary..."
  Rscript r/model_evaluation_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia evaluation readiness score..."
  julia julia/evaluation_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go model registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust model evaluation inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C prediction registry fingerprint..."
  cc c/fnv_prediction_registry_fingerprint.c -o outputs/fnv_prediction_registry_fingerprint
  ./outputs/fnv_prediction_registry_fingerprint data/binary_predictions.csv > outputs/fnv_prediction_registry_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ threshold metric adjacency..."
  c++ -std=c++17 cpp/threshold_metric_adjacency.cpp -o outputs/threshold_metric_adjacency
  ./outputs/threshold_metric_adjacency > outputs/threshold_metric_adjacency_cpp.txt
  cat outputs/threshold_metric_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto model evaluation template..."
  quarto render quarto/model-evaluation-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
