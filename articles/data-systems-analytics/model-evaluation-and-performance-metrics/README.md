# Model Evaluation and Performance Metrics

This companion code models evaluation as model-quality evidence infrastructure: metrics, thresholds, calibration, error distributions, regression loss, subgroup behavior, monitoring windows, and governance limits.

The examples use model registries, binary predictions, regression predictions, threshold policies, subgroup labels, calibration bins, monitoring windows, metric scorecards, and risk limits to show how teams can evaluate whether a predictive system is good enough for the task it is meant to perform.

## Included languages and examples

- `python/` — classification, calibration, threshold, regression, subgroup, and monitoring scorecard with manifest
- `r/` — threshold, confusion-matrix, calibration, and regression summaries
- `julia/` — evaluation readiness scoring
- `sql/` — schema and model-evaluation governance queries
- `go/` — model registry contract validation utility
- `rust/` — model status and task inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for prediction registries
- `cpp/` — threshold-policy and metric adjacency example
- `typescript/` — typed model, metric, threshold, calibration, and monitoring contracts
- `quarto/` — reproducible model evaluation report skeleton
- `terraform/` — non-deploying placeholder for model evaluation platform capabilities
- `bash/` — orchestration wrapper
- `docs/` — evaluation checklist, threshold policy, calibration review, and monitoring checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Evaluation turns prediction into evidence.

```text
task + prediction target + error costs
        → metrics + thresholds + calibration + subgroup checks
        → uncertainty + monitoring + governance limits
        → model quality decisions and lifecycle accountability
```

A mature model evaluation workflow does not ask only which model has the highest score. It asks which metric is appropriate, which threshold is acceptable, which errors matter, whether probabilities are calibrated, whether performance is stable across groups and time, and whether the model remains within risk limits after deployment.
