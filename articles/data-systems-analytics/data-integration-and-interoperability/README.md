# Data Integration and Interoperability

This companion code models data integration and interoperability as a coordination problem rather than as simple data movement.

The examples use source-system schemas, mapping rules, entity crosswalks, interoperability checks, lineage events, and message payloads to show how integration quality depends on schema alignment, identifier coherence, semantic translation, technical exchange, governance, observability, and boundary management.

## Included languages and examples

- `python/` — interoperability scorecard, mapping coverage, entity-linkage review, and manifest
- `r/` — integration coverage and quality summaries
- `julia/` — schema-mapping readiness scoring
- `sql/` — schema and integration governance queries
- `go/` — interoperability contract validation utility
- `rust/` — source-system and mapping inventory summarizer
- `c/` — deterministic FNV-1a fingerprinting for mapping registry files
- `cpp/` — integration dependency and lineage adjacency example
- `typescript/` — typed source, mapping, and interoperability contracts
- `terraform/` — non-deploying placeholder for integration platform resource categories
- `bash/` — orchestration wrapper
- `docs/` — integration canvas, mapping checklist, and governance checklist
- `ci/` — GitHub Actions smoke-test workflow

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Integration and interoperability should preserve meaning across boundaries:

```text
source systems → schema mappings → entity crosswalks → canonical/semantic model
        → lineage + quality + governance + access controls
        → interoperable analytics and operational use
```

Technical movement is not enough. A trustworthy integration layer must preserve identifiers, semantics, timing, lineage, and governance.
