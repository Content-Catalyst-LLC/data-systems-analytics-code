# Feature Engineering and Data Representation

This companion code models feature engineering as representation-integrity infrastructure: numerical transformations, categorical encodings, temporal and cyclical features, feature crosses, high-cardinality controls, leakage prevention, feature selection, compression, lineage, and governance review.

## Included languages and examples

- `python/` — feature engineering scorecard, transformation examples, leakage checks, and manifest
- `r/` — feature registry, encoding, temporal, leakage, and selection summaries
- `julia/` — representation readiness scoring
- `sql/` — schema and feature-governance queries
- `go/` — feature registry contract validation utility
- `rust/` — feature family and status inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for feature registries
- `cpp/` — feature-to-source adjacency example
- `typescript/` — typed feature, transform, leakage, and governance contracts
- `quarto/` — reproducible feature engineering report skeleton
- `terraform/` — non-deploying placeholder for feature-store capabilities
- `bash/` — orchestration wrapper
- `docs/` — feature engineering checklist, leakage checklist, and representation review canvas
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Representation determines what a model can learn.

```text
raw observations → transformation + encoding + aggregation
        → feature registry + leakage checks + lineage
        → train/validation/deployment consistency
        → more reliable model evidence and governance
```
