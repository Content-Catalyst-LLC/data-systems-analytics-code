.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/distributed_data_scorecard.py

sql:
	python3 sql/run_sqlite_distributed_data.py

r:
	Rscript r/distributed_data_summary.R

julia:
	julia julia/quorum_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_cluster_fingerprint.c -o outputs/fnv_cluster_fingerprint
	./outputs/fnv_cluster_fingerprint data/cluster_nodes.csv > outputs/fnv_cluster_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/shard_router.cpp -o outputs/shard_router
	./outputs/shard_router

quarto:
	quarto render quarto/distributed-data-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
