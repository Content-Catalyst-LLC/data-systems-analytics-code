# Predictive Analytics and Machine Learning Models

This companion code models predictive analytics as evidence infrastructure: supervised learning tasks, train/validation/test splits, model families, feature sets, loss functions, classification thresholds, calibration, rare-event behavior, drift monitoring, and predictive governance.

## Included languages and examples

- `python/` — predictive modeling scorecard with classification, regression, calibration, threshold, and drift summaries
- `r/` — supervised-learning registry, metric, threshold, and monitoring summaries
- `julia/` — predictive governance readiness scoring
- `sql/` — schema and predictive-model governance queries
- `go/` — predictive model registry contract validation utility
- `rust/` — task and model-family inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for prediction datasets
- `cpp/` — model-to-evidence adjacency example
- `typescript/` — typed predictive model, task, metric, threshold, and monitoring contracts
- `quarto/` — reproducible predictive analytics report skeleton
- `terraform/` — non-deploying placeholder for predictive-model platform capabilities
- `bash/` — orchestration wrapper
- `docs/` — predictive modeling checklist, leakage checklist, calibration review, monitoring checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Predictive analytics turns historical examples into claims about unseen cases.

```text
features + labels → training and validation
        → model selection + metrics + calibration + thresholds
        → monitoring + drift review + governance limits
        → responsible prediction under uncertainty
```

A mature predictive workflow does not ask only whether a model can fit the past. It asks whether the model generalizes, whether its probabilities are meaningful, whether thresholds match the decision context, whether errors are acceptable, and whether performance remains stable after deployment.
