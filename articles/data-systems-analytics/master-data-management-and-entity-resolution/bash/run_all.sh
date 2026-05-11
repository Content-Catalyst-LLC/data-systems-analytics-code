#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python MDM/entity-resolution scorecard..."
python3 python/mdm_entity_resolution_scorecard.py

echo "Loading SQLite MDM governance example..."
python3 sql/run_sqlite_mdm_entity_resolution.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R MDM summary..."
  Rscript r/mdm_entity_resolution_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia match confidence score..."
  julia julia/match_confidence_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go candidate match contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust MDM inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C candidate match fingerprint..."
  cc c/fnv_candidate_match_fingerprint.c -o outputs/fnv_candidate_match_fingerprint
  ./outputs/fnv_candidate_match_fingerprint data/candidate_matches.csv > outputs/fnv_candidate_match_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ entity hierarchy adjacency..."
  c++ -std=c++17 cpp/entity_hierarchy_adjacency.cpp -o outputs/entity_hierarchy_adjacency
  ./outputs/entity_hierarchy_adjacency > outputs/entity_hierarchy_adjacency_cpp.txt
  cat outputs/entity_hierarchy_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
