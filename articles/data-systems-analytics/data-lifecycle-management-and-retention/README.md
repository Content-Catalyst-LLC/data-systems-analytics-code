# Data Lifecycle Management and Retention

This article companion workflow demonstrates how data lifecycle management and retention can be represented as reproducible analytical operations.

The project includes:

- Python workflow for classifying data assets, applying retention rules, respecting legal holds, and generating disposition review registers.
- R workflow for lifecycle risk analysis, aging analysis, storage exposure review, and governance scorecards.
- SQL schema for modeling assets, retention rules, lifecycle review, legal holds, and disposition evidence.
- Sample data for retention assets and retention rules.
- Documentation for governance interpretation.

## Repository structure

```text
articles/data-lifecycle-management-and-retention/
├── data/
├── docs/
├── notebooks/
├── outputs/
├── python/
├── r/
└── sql/
```

## Python workflow

```bash
cd ~/Projects/data-systems-and-analytics-code/articles/data-lifecycle-management-and-retention
python3 -m venv .venv
source .venv/bin/activate
pip install -r python/requirements.txt
python python/data_lifecycle_retention_workflow.py
```

## R workflow

```bash
cd ~/Projects/data-systems-and-analytics-code/articles/data-lifecycle-management-and-retention
Rscript r/data_lifecycle_retention_audit.R
```

## SQL workflow

Run the SQL file in SQLite:

```bash
cd ~/Projects/data-systems-and-analytics-code/articles/data-lifecycle-management-and-retention
sqlite3 outputs/lifecycle_demo.sqlite < sql/data_lifecycle_schema.sql
```

## Governance note

Retention periods in these sample workflows are illustrative. Real retention schedules should be developed with legal, records-management, privacy, security, archival, and business review.
