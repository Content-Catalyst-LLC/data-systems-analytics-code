#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python distributed data scorecard..."
python3 python/distributed_data_scorecard.py

echo "Loading SQLite distributed data example..."
python3 sql/run_sqlite_distributed_data.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R distributed data summary..."
  Rscript r/distributed_data_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia quorum readiness score..."
  julia julia/quorum_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go cluster node validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust replica inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C cluster fingerprint..."
  cc c/fnv_cluster_fingerprint.c -o outputs/fnv_cluster_fingerprint
  ./outputs/fnv_cluster_fingerprint data/cluster_nodes.csv > outputs/fnv_cluster_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ shard router..."
  c++ -std=c++17 cpp/shard_router.cpp -o outputs/shard_router
  ./outputs/shard_router > outputs/shard_router_cpp.txt
  cat outputs/shard_router_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto distributed data template..."
  quarto render quarto/distributed-data-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
