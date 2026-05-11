#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python descriptive EDA scorecard..."
python3 python/descriptive_eda_scorecard.py

echo "Loading SQLite descriptive EDA example..."
python3 sql/run_sqlite_descriptive_eda.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R descriptive EDA summary..."
  Rscript r/descriptive_eda_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia exploration readiness score..."
  julia julia/exploration_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go exploration dataset validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust EDA inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C exploration dataset fingerprint..."
  cc c/fnv_exploration_dataset_fingerprint.c -o outputs/fnv_exploration_dataset_fingerprint
  ./outputs/fnv_exploration_dataset_fingerprint data/exploration_dataset.csv > outputs/fnv_exploration_dataset_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ exploration question adjacency..."
  c++ -std=c++17 cpp/exploration_question_adjacency.cpp -o outputs/exploration_question_adjacency
  ./outputs/exploration_question_adjacency > outputs/exploration_question_adjacency_cpp.txt
  cat outputs/exploration_question_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto descriptive EDA template..."
  quarto render quarto/descriptive-eda-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
