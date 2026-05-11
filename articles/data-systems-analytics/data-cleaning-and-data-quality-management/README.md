# Data Cleaning and Data Quality Management

This companion code models data quality management as evidence infrastructure: profiling, dimensions, validation rules, duplicate/entity-resolution review, survivorship, rejected-record quarantine, root-cause tracking, monitoring, stewardship, and quality-readiness scoring.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Cleaning repairs records. Quality management improves the system that produces them.

```text
raw records → profiling → validation rules + quality dimensions
        → cleaning / standardization / deduplication
        → rejects + stewardship + root-cause records
        → monitoring, lineage, readiness scoring, and governance review
```

A mature quality workflow does not only produce a cleaner table. It preserves evidence about defects, remediation, unresolved uncertainty, business impact, and upstream process causes.
