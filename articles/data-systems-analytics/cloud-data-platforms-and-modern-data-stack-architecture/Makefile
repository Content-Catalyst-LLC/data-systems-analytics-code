.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/platform_scorecard.py

sql:
	python3 sql/run_sqlite_architecture.py

r:
	Rscript r/platform_summary.R

julia:
	julia julia/platform_dependency_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_architecture_fingerprint.c -o outputs/fnv_architecture_fingerprint
	./outputs/fnv_architecture_fingerprint data/stack_components.csv > outputs/fnv_architecture_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/layer_dependency_order.cpp -o outputs/layer_dependency_order
	./outputs/layer_dependency_order

clean:
	find outputs -type f ! -name ".gitkeep" -delete
