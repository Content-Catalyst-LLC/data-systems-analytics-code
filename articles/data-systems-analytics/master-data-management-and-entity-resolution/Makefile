.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/mdm_entity_resolution_scorecard.py

sql:
	python3 sql/run_sqlite_mdm_entity_resolution.py

r:
	Rscript r/mdm_entity_resolution_summary.R

julia:
	julia julia/match_confidence_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_candidate_match_fingerprint.c -o outputs/fnv_candidate_match_fingerprint
	./outputs/fnv_candidate_match_fingerprint data/candidate_matches.csv > outputs/fnv_candidate_match_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/entity_hierarchy_adjacency.cpp -o outputs/entity_hierarchy_adjacency
	./outputs/entity_hierarchy_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
