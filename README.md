# Data Systems & Analytics Code

A companion multi-language code repository for the Data Systems & Analytics knowledge series.

This repository demonstrates practical analytical infrastructure for modern data systems:

- SQL schemas, seed data, analytical views, and data-quality checks
- Python ETL, profiling, validation, feature generation, and reproducible reports
- R exploratory analysis and statistical reporting
- Julia numerical and time-series workflows
- Rust CSV/schema validation CLI
- Go streaming event simulation
- TypeScript dashboard scaffold
- YAML metadata for data contracts, lineage, and workflows
- notebooks, docs, outputs, and article-roadmap metadata

The repo is intentionally local-first. It is designed to run without proprietary cloud services.

## Quick Start

```bash
# Build local SQLite database
sqlite3 data_systems.db < sql/schema.sql
sqlite3 data_systems.db < sql/seed_data_systems.sql
sqlite3 data_systems.db < sql/views.sql
sqlite3 data_systems.db < sql/data_quality_checks.sql

# Run Python workflow
python3 python/src/etl_pipeline.py --db data_systems.db --output-dir outputs
python3 python/src/profile_dataset.py --db data_systems.db --output outputs/data-profile.md
python3 python/src/export_article_roadmap.py --db data_systems.db --output outputs/article-roadmap.md

# Run R workflow
Rscript r/analytics_summary.R

# Optional advanced workflows
julia julia/time_series_workflow.jl
go run go/streaming_events.go
cargo run --manifest-path rust/Cargo.toml -- data/raw/observations.csv
```

## Repository Structure

- `articles/data-systems-analytics/` — Article planning notes
- `data/` — Raw, processed, and reference datasets
- `docs/` — Methodology, source hierarchy, workflow notes, governance notes
- `sql/` — Schema, seed data, views, analytical queries, quality checks
- `python/` — ETL, profiling, validation, exports, tests
- `r/` — Statistical summaries and reporting
- `julia/` — Numerical/time-series examples
- `rust/` — CLI validation tool
- `go/` — Streaming event simulation
- `typescript/` — Dashboard scaffold
- `configs/` — Data contracts, lineage, workflow configuration
- `schemas/` — JSON schema and data-contract references
- `notebooks/` — Reproducible notebook starters
- `outputs/` — Generated reports and tables

## License

Code is released under the MIT License. Original documentation and metadata are covered by `CONTENT_LICENSE.md`.
