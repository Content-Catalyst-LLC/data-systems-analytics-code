.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/interoperability_scorecard.py

sql:
	python3 sql/run_sqlite_interoperability.py

r:
	Rscript r/integration_quality_summary.R

julia:
	julia julia/mapping_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_mapping_registry_fingerprint.c -o outputs/fnv_mapping_registry_fingerprint
	./outputs/fnv_mapping_registry_fingerprint data/schema_mappings.csv > outputs/fnv_mapping_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/lineage_adjacency.cpp -o outputs/lineage_adjacency
	./outputs/lineage_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
