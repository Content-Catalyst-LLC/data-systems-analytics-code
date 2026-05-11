.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/governance_stewardship_scorecard.py

sql:
	python3 sql/run_sqlite_governance_stewardship.py

r:
	Rscript r/governance_stewardship_summary.R

julia:
	julia julia/stewardship_maturity_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_governance_register_fingerprint.c -o outputs/fnv_governance_register_fingerprint
	./outputs/fnv_governance_register_fingerprint data/policy_register.csv > outputs/fnv_governance_register_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/decision_rights_adjacency.cpp -o outputs/decision_rights_adjacency
	./outputs/decision_rights_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
