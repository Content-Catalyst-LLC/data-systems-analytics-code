.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/etl_transformation_scorecard.py

sql:
	python3 sql/run_sqlite_etl_transformation.py

r:
	Rscript r/etl_transformation_summary.R

julia:
	julia julia/etl_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_extract_fingerprint.c -o outputs/fnv_extract_fingerprint
	./outputs/fnv_extract_fingerprint data/raw_customer_extract.csv > outputs/fnv_extract_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/transformation_lineage_adjacency.cpp -o outputs/transformation_lineage_adjacency
	./outputs/transformation_lineage_adjacency

quarto:
	quarto render quarto/etl-transformation-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
