.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/metadata_catalog_lineage_scorecard.py

sql:
	python3 sql/run_sqlite_metadata_catalog_lineage.py

r:
	Rscript r/metadata_catalog_lineage_summary.R

julia:
	julia julia/metadata_maturity_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_metadata_registry_fingerprint.c -o outputs/fnv_metadata_registry_fingerprint
	./outputs/fnv_metadata_registry_fingerprint data/data_assets.csv > outputs/fnv_metadata_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/lineage_adjacency.cpp -o outputs/lineage_adjacency
	./outputs/lineage_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
