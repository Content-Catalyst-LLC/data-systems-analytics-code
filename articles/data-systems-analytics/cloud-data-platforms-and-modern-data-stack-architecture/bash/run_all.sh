#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python cloud platform scorecard..."
python3 python/platform_scorecard.py

echo "Loading SQLite architecture example..."
python3 sql/run_sqlite_architecture.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R platform summary..."
  Rscript r/platform_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia dependency score..."
  julia julia/platform_dependency_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go stack validator..."
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
  echo "Compiling and running C architecture fingerprint..."
  cc c/fnv_architecture_fingerprint.c -o outputs/fnv_architecture_fingerprint
  ./outputs/fnv_architecture_fingerprint data/stack_components.csv > outputs/fnv_architecture_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ dependency ordering..."
  c++ -std=c++17 cpp/layer_dependency_order.cpp -o outputs/layer_dependency_order
  ./outputs/layer_dependency_order > outputs/layer_dependency_order.txt
  cat outputs/layer_dependency_order.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
