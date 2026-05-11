# Data Warehouses and Data Lakes

This companion code models warehouses, lakes, and lakehouse-style architectures as analytical estate governance infrastructure: raw zones, curated warehouse marts, dimensional models, table formats, metadata coverage, schema strategy, data-swamp risk, cost/performance profiles, lifecycle status, and readiness scoring.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Warehouses and lakes solve different analytical readiness problems.

```text
source systems → lake landing / raw retention
        → validation, metadata, lifecycle, and governance controls
        → refined zones, lakehouse tables, warehouse marts
        → dashboards, BI, data science, ML, archives, and decision support
```

A mature architecture does not choose storage ideology blindly. It distinguishes raw optionality, curated analytical state, dimensional structure, open table governance, performance requirements, and downstream trust.
