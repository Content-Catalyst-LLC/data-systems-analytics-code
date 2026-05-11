.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/causal_inference_scorecard.py

sql:
	python3 sql/run_sqlite_causal_inference.py

r:
	Rscript r/causal_inference_summary.R

julia:
	julia julia/causal_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_causal_registry_fingerprint.c -o outputs/fnv_causal_registry_fingerprint
	./outputs/fnv_causal_registry_fingerprint data/causal_study_registry.csv > outputs/fnv_causal_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/causal_design_adjacency.cpp -o outputs/causal_design_adjacency
	./outputs/causal_design_adjacency

quarto:
	quarto render quarto/causal-inference-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
