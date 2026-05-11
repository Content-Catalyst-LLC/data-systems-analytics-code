.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/predictive_model_scorecard.py

sql:
	python3 sql/run_sqlite_predictive_analytics.py

r:
	Rscript r/predictive_analytics_summary.R

julia:
	julia julia/predictive_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_prediction_dataset_fingerprint.c -o outputs/fnv_prediction_dataset_fingerprint
	./outputs/fnv_prediction_dataset_fingerprint data/classification_predictions.csv > outputs/fnv_prediction_dataset_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/model_evidence_adjacency.cpp -o outputs/model_evidence_adjacency
	./outputs/model_evidence_adjacency

quarto:
	quarto render quarto/predictive-analytics-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
