.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/reproducible_workflow.py --group-by system

sql:
	python3 sql/run_sqlite_workflow.py

r:
	Rscript r/reproducible_workflow.R

julia:
	julia julia/reproducible_workflow.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_fingerprint.c -o outputs/fnv_fingerprint
	./outputs/fnv_fingerprint data/sample_events.csv > outputs/fnv_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/reproducible_summary.cpp -o outputs/reproducible_summary_cpp
	./outputs/reproducible_summary_cpp

clean:
	rm -rf outputs/* data/snapshots
