.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/visualization_integrity_scorecard.py

sql:
	python3 sql/run_sqlite_visualization_integrity.py

r:
	Rscript r/visualization_communication_summary.R

julia:
	julia julia/visualization_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_visualization_registry_fingerprint.c -o outputs/fnv_visualization_registry_fingerprint
	./outputs/fnv_visualization_registry_fingerprint data/visualization_inventory.csv > outputs/fnv_visualization_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/chart_evidence_adjacency.cpp -o outputs/chart_evidence_adjacency
	./outputs/chart_evidence_adjacency

quarto:
	quarto render quarto/visualization-communication-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
