.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/model_evaluation_scorecard.py

sql:
	python3 sql/run_sqlite_model_evaluation.py

r:
	Rscript r/model_evaluation_summary.R

julia:
	julia julia/evaluation_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_prediction_registry_fingerprint.c -o outputs/fnv_prediction_registry_fingerprint
	./outputs/fnv_prediction_registry_fingerprint data/binary_predictions.csv > outputs/fnv_prediction_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/threshold_metric_adjacency.cpp -o outputs/threshold_metric_adjacency
	./outputs/threshold_metric_adjacency

quarto:
	quarto render quarto/model-evaluation-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
