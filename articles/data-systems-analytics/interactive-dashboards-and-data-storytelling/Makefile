.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/dashboard_storytelling_scorecard.py

sql:
	python3 sql/run_sqlite_dashboard_storytelling.py

r:
	Rscript r/dashboard_storytelling_summary.R

julia:
	julia julia/dashboard_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_dashboard_registry_fingerprint.c -o outputs/fnv_dashboard_registry_fingerprint
	./outputs/fnv_dashboard_registry_fingerprint data/dashboard_inventory.csv > outputs/fnv_dashboard_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/story_evidence_adjacency.cpp -o outputs/story_evidence_adjacency
	./outputs/story_evidence_adjacency

quarto:
	quarto render quarto/dashboard-story-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
