.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/feature_engineering_scorecard.py

sql:
	python3 sql/run_sqlite_feature_engineering.py

r:
	Rscript r/feature_engineering_summary.R

julia:
	julia julia/representation_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_feature_registry_fingerprint.c -o outputs/fnv_feature_registry_fingerprint
	./outputs/fnv_feature_registry_fingerprint data/feature_registry.csv > outputs/fnv_feature_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/feature_source_adjacency.cpp -o outputs/feature_source_adjacency
	./outputs/feature_source_adjacency

quarto:
	quarto render quarto/feature-engineering-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
