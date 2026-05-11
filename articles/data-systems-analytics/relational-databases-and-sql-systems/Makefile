.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/relational_sql_scorecard.py

sql:
	python3 sql/run_sqlite_relational.py

r:
	Rscript r/relational_sql_summary.R

julia:
	julia julia/relational_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_relational_schema_fingerprint.c -o outputs/fnv_relational_schema_fingerprint
	./outputs/fnv_relational_schema_fingerprint data/relational_schema_inventory.csv > outputs/fnv_relational_schema_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/relational_graph_adjacency.cpp -o outputs/relational_graph_adjacency
	./outputs/relational_graph_adjacency

quarto:
	quarto render quarto/relational-sql-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
