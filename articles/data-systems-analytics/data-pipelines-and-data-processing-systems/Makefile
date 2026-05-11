.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/pipeline_processing_scorecard.py

sql:
	python3 sql/run_sqlite_pipeline_processing.py

r:
	Rscript r/pipeline_processing_summary.R

julia:
	julia julia/pipeline_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_pipeline_fingerprint.c -o outputs/fnv_pipeline_fingerprint
	./outputs/fnv_pipeline_fingerprint data/pipeline_stages.csv > outputs/fnv_pipeline_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/pipeline_graph_adjacency.cpp -o outputs/pipeline_graph_adjacency
	./outputs/pipeline_graph_adjacency

quarto:
	quarto render quarto/pipeline-processing-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
