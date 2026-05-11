# Data Quality Metrics and Observability

This companion code models data quality and observability as operational assurance for modern data products.

The examples use dataset registries, quality checks, observability events, baselines, incident records, lineage records, and consumer-impact logs to show how teams can evaluate freshness, completeness, validity, uniqueness, schema drift, distribution drift, incident severity, lineage-aware impact, and remediation performance.

## Included languages and examples

- `python/` — quality and observability scorecard, incident and drift review, and manifest
- `r/` — quality dimension, incident, baseline, and remediation summaries
- `julia/` — dataset reliability scoring
- `sql/` — schema and quality governance queries
- `go/` — quality check contract validation utility
- `rust/` — incident and check inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for quality-check registries
- `cpp/` — lineage-aware impact adjacency example
- `typescript/` — typed dataset, check, incident, and observability contracts
- `terraform/` — non-deploying placeholder for observability platform resources
- `bash/` — orchestration wrapper
- `docs/` — quality canvas, incident review checklist, observability checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Quality and observability preserve trust over time:

```text
critical datasets → quality checks + baselines + lineage
        → alerts + incident triage + root cause
        → remediation + communication + learning
```

A mature data platform does not only test whether pipelines ran. It asks whether data remains fit for use, whether defects are visible, and whether remediation is accountable.
