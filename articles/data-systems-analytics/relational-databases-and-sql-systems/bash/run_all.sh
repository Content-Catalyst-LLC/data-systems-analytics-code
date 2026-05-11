#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python relational SQL scorecard..."
python3 python/relational_sql_scorecard.py

echo "Loading SQLite relational example..."
python3 sql/run_sqlite_relational.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R relational SQL summary..."
  Rscript r/relational_sql_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia relational readiness score..."
  julia julia/relational_readiness_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go schema inventory validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust constraint inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C schema fingerprint..."
  cc c/fnv_relational_schema_fingerprint.c -o outputs/fnv_relational_schema_fingerprint
  ./outputs/fnv_relational_schema_fingerprint data/relational_schema_inventory.csv > outputs/fnv_relational_schema_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ relational graph adjacency..."
  c++ -std=c++17 cpp/relational_graph_adjacency.cpp -o outputs/relational_graph_adjacency
  ./outputs/relational_graph_adjacency > outputs/relational_graph_adjacency_cpp.txt
  cat outputs/relational_graph_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v quarto >/dev/null 2>&1; then
  echo "Rendering Quarto relational SQL template..."
  quarto render quarto/relational-sql-template.qmd --output-dir ../outputs
else
  echo "Skipping Quarto render: quarto not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
