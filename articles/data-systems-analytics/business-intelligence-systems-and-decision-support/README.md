# Business Intelligence Systems and Decision Support

This companion code models business intelligence as decision infrastructure rather than as a dashboard-only reporting layer.

The examples use a small BI metric catalog, dashboard inventory, decision-threshold table, alert log, and decision-review dataset to show how business intelligence systems can be evaluated for decision support quality, metric trust, freshness, uncertainty visibility, governance, and organizational learning.

## Included languages and examples

- `python/` — decision-support scorecard, metric trust, dashboard review, and manifest
- `r/` — BI usage, alert, and decision-review summaries
- `julia/` — decision-support readiness scoring
- `sql/` — schema and BI governance queries
- `go/` — dashboard contract validation utility
- `rust/` — metric ownership and alert inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for BI registry files
- `cpp/` — alert routing and decision pathway adjacency example
- `typescript/` — typed BI metric and dashboard contracts
- `terraform/` — non-deploying placeholder for BI platform resource categories
- `bash/` — orchestration wrapper
- `docs/` — decision-support canvas, dashboard review checklist, and governance checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

High-trust BI connects data architecture to accountable decision routines:

```text
source data → governed metrics → dashboard/report/interface
        → threshold / alert / scenario review
        → decision owner → action / learning loop
```

A BI system should be judged not only by visualization quality, but by whether it improves decision clarity, traceability, timeliness, uncertainty awareness, and accountability.
