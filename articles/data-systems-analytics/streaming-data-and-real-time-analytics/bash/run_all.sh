#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python streaming analytics scorecard..."
python3 python/streaming_analytics_scorecard.py

echo "Loading SQLite streaming analytics example..."
python3 sql/run_sqlite_streaming_analytics.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R streaming analytics summary..."
  Rscript r/streaming_analytics_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia streaming readiness score..."
  julia julia/streaming_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go event stream validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust streaming event inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C event stream fingerprint..."
  cc c/fnv_event_stream_fingerprint.c -o outputs/fnv_event_stream_fingerprint
  ./outputs/fnv_event_stream_fingerprint data/event_stream.csv > outputs/fnv_event_stream_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ window policy adjacency..."
  c++ -std=c++17 cpp/window_policy_adjacency.cpp -o outputs/window_policy_adjacency
  ./outputs/window_policy_adjacency > outputs/window_policy_adjacency_cpp.txt
  cat outputs/window_policy_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto streaming analytics template..."
  quarto render quarto/streaming-analytics-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
