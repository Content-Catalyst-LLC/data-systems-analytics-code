#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python pipeline processing scorecard..."
python3 python/pipeline_processing_scorecard.py

echo "Loading SQLite pipeline processing example..."
python3 sql/run_sqlite_pipeline_processing.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R pipeline processing summary..."
  Rscript r/pipeline_processing_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia pipeline readiness score..."
  julia julia/pipeline_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go pipeline stage validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust pipeline inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C pipeline fingerprint..."
  cc c/fnv_pipeline_fingerprint.c -o outputs/fnv_pipeline_fingerprint
  ./outputs/fnv_pipeline_fingerprint data/pipeline_stages.csv > outputs/fnv_pipeline_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ pipeline graph adjacency..."
  c++ -std=c++17 cpp/pipeline_graph_adjacency.cpp -o outputs/pipeline_graph_adjacency
  ./outputs/pipeline_graph_adjacency > outputs/pipeline_graph_adjacency_cpp.txt
  cat outputs/pipeline_graph_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto pipeline processing template..."
  quarto render quarto/pipeline-processing-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
