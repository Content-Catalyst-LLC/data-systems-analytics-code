.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/decision_support_scorecard.py

sql:
	python3 sql/run_sqlite_bi.py

r:
	Rscript r/bi_usage_decision_review.R

julia:
	julia julia/bi_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_bi_registry_fingerprint.c -o outputs/fnv_bi_registry_fingerprint
	./outputs/fnv_bi_registry_fingerprint data/dashboard_inventory.csv > outputs/fnv_bi_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/alert_pathway_summary.cpp -o outputs/alert_pathway_summary
	./outputs/alert_pathway_summary

clean:
	find outputs -type f ! -name ".gitkeep" -delete
