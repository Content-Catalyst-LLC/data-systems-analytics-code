.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/semantic_layer_scorecard.py

sql:
	python3 sql/run_sqlite_semantic_layer.py

r:
	Rscript r/semantic_layer_summary.R

julia:
	julia julia/semantic_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_semantic_metric_fingerprint.c -o outputs/fnv_semantic_metric_fingerprint
	./outputs/fnv_semantic_metric_fingerprint data/semantic_metrics.csv > outputs/fnv_semantic_metric_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/semantic_lineage_adjacency.cpp -o outputs/semantic_lineage_adjacency
	./outputs/semantic_lineage_adjacency

clean:
	find outputs -type f ! -name ".gitkeep" -delete
