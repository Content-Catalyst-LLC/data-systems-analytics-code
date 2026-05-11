.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/warehouse_lake_scorecard.py

sql:
	python3 sql/run_sqlite_warehouse_lake.py

r:
	Rscript r/warehouse_lake_summary.R

julia:
	julia julia/warehouse_lake_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_warehouse_lake_fingerprint.c -o outputs/fnv_warehouse_lake_fingerprint
	./outputs/fnv_warehouse_lake_fingerprint data/data_assets.csv > outputs/fnv_warehouse_lake_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/star_schema_adjacency.cpp -o outputs/star_schema_adjacency
	./outputs/star_schema_adjacency

quarto:
	quarto render quarto/warehouse-lake-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
