#!/usr/bin/env bash
set -euo pipefail

sqlite3 data_systems.db < sql/schema.sql
sqlite3 data_systems.db < sql/seed_data_systems.sql
sqlite3 data_systems.db < sql/views.sql
sqlite3 data_systems.db < sql/data_quality_checks.sql

python3 python/src/etl_pipeline.py --db data_systems.db --output-dir outputs
python3 python/src/profile_dataset.py --db data_systems.db --output outputs/data-profile.md
python3 python/src/export_article_roadmap.py --db data_systems.db --output outputs/article-roadmap.md
python3 python/src/feature_generation.py --db data_systems.db --output data/processed/system_features.csv

Rscript r/analytics_summary.R || true
julia julia/time_series_workflow.jl || true
go run go/streaming_events.go || true

echo "Workflow complete."
