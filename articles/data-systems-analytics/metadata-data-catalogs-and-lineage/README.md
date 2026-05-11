# Metadata, Data Catalogs, and Lineage

This companion code models metadata, data catalogs, and lineage as epistemic infrastructure for modern data systems.

The examples use asset metadata, catalog entries, glossary terms, lineage edges, provenance events, policy tags, quality signals, and usage records to show how organizations can evaluate asset legibility, catalog trust, lineage depth, governance coverage, provenance completeness, and downstream impact.

## Included languages and examples

- `python/` — metadata trust and lineage scorecard with manifest
- `r/` — catalog, glossary, policy, lineage, and usage summaries
- `julia/` — metadata maturity scoring
- `sql/` — schema and metadata-governance queries
- `go/` — metadata asset contract validation utility
- `rust/` — domain and classification inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for metadata registries
- `cpp/` — lineage adjacency example
- `typescript/` — typed metadata, catalog, lineage, and provenance contracts
- `terraform/` — non-deploying placeholder for metadata platform resources
- `bash/` — orchestration wrapper
- `docs/` — metadata canvas, catalog review checklist, lineage checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Metadata makes assets legible. Catalogs make them navigable. Lineage makes them traceable.

```text
data assets → metadata + glossary + policy tags
        → catalog entry + quality signals + usage context
        → lineage edges + provenance events
        → governance, analytics, audit, and AI readiness
```

A mature metadata system does not only document data. It helps govern meaning, trust, ownership, impact, and accountable use.
