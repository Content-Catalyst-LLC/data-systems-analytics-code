.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/security_privacy_access_scorecard.py

sql:
	python3 sql/run_sqlite_security_privacy.py

r:
	Rscript r/privacy_access_summary.R

julia:
	julia julia/access_risk_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_access_policy_fingerprint.c -o outputs/fnv_access_policy_fingerprint
	./outputs/fnv_access_policy_fingerprint data/access_policies.csv > outputs/fnv_access_policy_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/sensitive_flow_adjacency.cpp -o outputs/sensitive_flow_adjacency
	./outputs/sensitive_flow_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
