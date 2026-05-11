.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/database_architecture_scorecard.py

sql:
	python3 sql/run_sqlite_database_architecture.py

r:
	Rscript r/database_architecture_summary.R

julia:
	julia julia/database_architecture_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_database_architecture_fingerprint.c -o outputs/fnv_database_architecture_fingerprint
	./outputs/fnv_database_architecture_fingerprint data/system_inventory.csv > outputs/fnv_database_architecture_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/architecture_lineage_adjacency.cpp -o outputs/architecture_lineage_adjacency
	./outputs/architecture_lineage_adjacency

quarto:
	quarto render quarto/database-architecture-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
