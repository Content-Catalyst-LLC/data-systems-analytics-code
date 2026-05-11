# Master Data Management and Entity Resolution

This companion code models master data management and entity resolution as representational governance rather than simple deduplication.

The examples use source records, match candidates, entity crosswalks, survivorship rules, legal identifiers, hierarchy edges, stewardship queues, privacy-risk records, and lineage events to show how organizations can evaluate match confidence, merge risk, survivorship quality, hierarchy coherence, review burden, provenance, and identity-governance risk.

## Included languages and examples

- `python/` — MDM/entity-resolution scorecard, match-risk review, and manifest
- `r/` — source-system, match-confidence, survivorship, and stewardship summaries
- `julia/` — match confidence and merge-action scoring
- `sql/` — schema and MDM governance queries
- `go/` — source record and candidate match contract validation utility
- `rust/` — domain and stewardship inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for candidate-match registries
- `cpp/` — entity hierarchy and lineage adjacency example
- `typescript/` — typed entity, match, survivorship, and stewardship contracts
- `terraform/` — non-deploying placeholder for MDM platform resource categories
- `bash/` — orchestration wrapper
- `docs/` — MDM canvas, match review checklist, survivorship checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

MDM and entity resolution stabilize organizational reference objects:

```text
source records → standardized attributes → candidate matches
        → steward-reviewed links + survivorship rules
        → mastered entities + hierarchies + lineage
        → analytics, operations, governance, and AI use
```

A high-maturity MDM program distinguishes probabilistic similarity from governance action. A high match score is not automatically a safe merge.
