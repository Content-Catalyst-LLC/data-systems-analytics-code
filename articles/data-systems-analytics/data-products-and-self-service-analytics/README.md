# Data Products and Self-Service Analytics

This companion code models data products and self-service analytics as a governed analytical operating system rather than as a dashboard-only strategy.

The examples use a small product registry, semantic metrics catalog, access-event table, quality-check inventory, and lineage map to show how reusable analytical products can be documented, scored, governed, and exposed through self-service interfaces.

## Included languages and examples

- `python/` — data product scorecard, quality coverage, usage summary, and manifest
- `r/` — domain and product-lifecycle summaries
- `julia/` — product readiness scoring example
- `sql/` — schema and governance queries
- `go/` — product contract validation utility
- `rust/` — ownership and usage inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for product registry files
- `cpp/` — lineage adjacency and dependency summary
- `typescript/` — typed data product and semantic metric contracts
- `terraform/` — non-deploying placeholder for product platform resource categories
- `bash/` — orchestration wrapper
- `docs/` — product canvas, governance checklist, and lifecycle checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Self-service analytics is strongest when it sits on top of governed products:

```text
source systems → ingestion → curated data product → semantic metrics
        → quality / lineage / access controls
        → self-service dashboards, notebooks, APIs, and decision support
```

A useful data product should have ownership, purpose, documented semantics, quality expectations, access policy, lifecycle status, and measurable consumer use.
