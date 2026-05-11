.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/descriptive_eda_scorecard.py

sql:
	python3 sql/run_sqlite_descriptive_eda.py

r:
	Rscript r/descriptive_eda_summary.R

julia:
	julia julia/exploration_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_exploration_dataset_fingerprint.c -o outputs/fnv_exploration_dataset_fingerprint
	./outputs/fnv_exploration_dataset_fingerprint data/exploration_dataset.csv > outputs/fnv_exploration_dataset_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/exploration_question_adjacency.cpp -o outputs/exploration_question_adjacency
	./outputs/exploration_question_adjacency

quarto:
	quarto render quarto/descriptive-eda-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
