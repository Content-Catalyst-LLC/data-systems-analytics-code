#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python statistical inference scorecard..."
python3 python/statistical_inference_scorecard.py

echo "Loading SQLite statistical inference example..."
python3 sql/run_sqlite_statistical_inference.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R statistical inference summary..."
  Rscript r/statistical_inference_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia inference readiness score..."
  julia julia/inference_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go statistical model registry contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust statistical model inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C inference data fingerprint..."
  cc c/fnv_inference_data_fingerprint.c -o outputs/fnv_inference_data_fingerprint
  ./outputs/fnv_inference_data_fingerprint data/sample_observations.csv > outputs/fnv_inference_data_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ inference claim adjacency..."
  c++ -std=c++17 cpp/inference_claim_adjacency.cpp -o outputs/inference_claim_adjacency
  ./outputs/inference_claim_adjacency > outputs/inference_claim_adjacency_cpp.txt
  cat outputs/inference_claim_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto statistical inference template..."
  quarto render quarto/statistical-inference-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
