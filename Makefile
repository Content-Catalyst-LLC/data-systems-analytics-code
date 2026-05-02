DB=data_systems.db

.PHONY: db python r julia go rust all clean

db:
	sqlite3 $(DB) < sql/schema.sql
	sqlite3 $(DB) < sql/seed_data_systems.sql
	sqlite3 $(DB) < sql/views.sql
	sqlite3 $(DB) < sql/data_quality_checks.sql

python: db
	python3 python/src/etl_pipeline.py --db $(DB) --output-dir outputs
	python3 python/src/profile_dataset.py --db $(DB) --output outputs/data-profile.md
	python3 python/src/export_article_roadmap.py --db $(DB) --output outputs/article-roadmap.md
	python3 python/src/feature_generation.py --db $(DB) --output data/processed/system_features.csv

r:
	Rscript r/analytics_summary.R

julia:
	julia julia/time_series_workflow.jl

go:
	go run go/streaming_events.go

rust:
	cargo run --manifest-path rust/Cargo.toml -- data/raw/observations.csv

all: python r julia go rust

clean:
	rm -f $(DB)
	rm -f outputs/*
	touch outputs/.gitkeep
