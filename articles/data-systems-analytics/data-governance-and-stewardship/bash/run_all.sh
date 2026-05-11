#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python governance/stewardship scorecard..."
python3 python/governance_stewardship_scorecard.py

echo "Loading SQLite governance example..."
python3 sql/run_sqlite_governance_stewardship.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R governance/stewardship summary..."
  Rscript r/governance_stewardship_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia stewardship maturity score..."
  julia julia/stewardship_maturity_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go governance contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust governance inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C governance register fingerprint..."
  cc c/fnv_governance_register_fingerprint.c -o outputs/fnv_governance_register_fingerprint
  ./outputs/fnv_governance_register_fingerprint data/policy_register.csv > outputs/fnv_governance_register_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ decision-rights adjacency..."
  c++ -std=c++17 cpp/decision_rights_adjacency.cpp -o outputs/decision_rights_adjacency
  ./outputs/decision_rights_adjacency > outputs/decision_rights_adjacency_cpp.txt
  cat outputs/decision_rights_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
