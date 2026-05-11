.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/quality_observability_scorecard.py

sql:
	python3 sql/run_sqlite_quality_observability.py

r:
	Rscript r/quality_observability_summary.R

julia:
	julia julia/dataset_reliability_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_quality_check_fingerprint.c -o outputs/fnv_quality_check_fingerprint
	./outputs/fnv_quality_check_fingerprint data/quality_checks.csv > outputs/fnv_quality_check_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/lineage_impact_adjacency.cpp -o outputs/lineage_impact_adjacency
	./outputs/lineage_impact_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
