# ETL and Data Transformation Systems

This companion code models ETL/ELT as transformation evidence infrastructure: raw extracts, staging tables, canonical targets, semantic mappings, data-quality gates, CDC events, idempotent merge rules, rejected-record quarantine, lineage records, orchestration metadata, and transformation-readiness scoring.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Transformation systems turn heterogeneous operational traces into governed analytical state.

```text
sources → raw extracts / CDC events → staging
        → quality gates + semantic mappings
        → canonical targets + merge logic
        → lineage, rejects, orchestration, and governance review
```

A mature transformation workflow does not only move records. It preserves meaning, explains rejected data, supports replay, makes mappings testable, and records which logic produced downstream state.
