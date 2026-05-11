#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p outputs

echo "Running Python security/privacy/access scorecard..."
python3 python/security_privacy_access_scorecard.py

echo "Loading SQLite security/privacy governance example..."
python3 sql/run_sqlite_security_privacy.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R privacy and access summary..."
  Rscript r/privacy_access_summary.R
else
  echo "Skipping R workflow: Rscript not found"
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia access risk score..."
  julia julia/access_risk_score.jl
else
  echo "Skipping Julia workflow: julia not found"
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go access policy contract validator..."
  (cd go && go run .)
else
  echo "Skipping Go workflow: go not found"
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust entitlement inventory..."
  (cd rust && cargo run)
else
  echo "Skipping Rust workflow: cargo not found"
fi

if command -v cc >/dev/null 2>&1; then
  echo "Compiling and running C access policy fingerprint..."
  cc c/fnv_access_policy_fingerprint.c -o outputs/fnv_access_policy_fingerprint
  ./outputs/fnv_access_policy_fingerprint data/access_policies.csv > outputs/fnv_access_policy_fingerprint.txt
else
  echo "Skipping C example: cc not found"
fi

if command -v c++ >/dev/null 2>&1; then
  echo "Compiling and running C++ sensitive flow adjacency..."
  c++ -std=c++17 cpp/sensitive_flow_adjacency.cpp -o outputs/sensitive_flow_adjacency
  ./outputs/sensitive_flow_adjacency > outputs/sensitive_flow_adjacency_cpp.txt
  cat outputs/sensitive_flow_adjacency_cpp.txt
else
  echo "Skipping C++ example: c++ not found"
fi

if command -v npm >/dev/null 2>&1; then
  echo "TypeScript contract is present. Install dependencies with: cd typescript && npm install && npm run check"
else
  echo "Skipping TypeScript check: npm not found"
fi

echo "Done. Review generated files in outputs/."
