.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/data_quality_scorecard.py

sql:
	python3 sql/run_sqlite_data_quality.py

r:
	Rscript r/data_quality_summary.R

julia:
	julia julia/data_quality_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_data_quality_fingerprint.c -o outputs/fnv_data_quality_fingerprint
	./outputs/fnv_data_quality_fingerprint data/raw_customer_records.csv > outputs/fnv_data_quality_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/quality_rule_adjacency.cpp -o outputs/quality_rule_adjacency
	./outputs/quality_rule_adjacency

quarto:
	quarto render quarto/data-quality-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
