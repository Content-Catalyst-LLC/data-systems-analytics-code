.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/statistical_inference_scorecard.py

sql:
	python3 sql/run_sqlite_statistical_inference.py

r:
	Rscript r/statistical_inference_summary.R

julia:
	julia julia/inference_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_inference_data_fingerprint.c -o outputs/fnv_inference_data_fingerprint
	./outputs/fnv_inference_data_fingerprint data/sample_observations.csv > outputs/fnv_inference_data_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/inference_claim_adjacency.cpp -o outputs/inference_claim_adjacency
	./outputs/inference_claim_adjacency

quarto:
	quarto render quarto/statistical-inference-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
