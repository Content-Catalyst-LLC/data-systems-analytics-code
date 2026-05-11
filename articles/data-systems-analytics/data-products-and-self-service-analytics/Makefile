.PHONY: run python sql r julia go rust c cpp clean

run:
	bash bash/run_all.sh

python:
	python3 python/product_scorecard.py

sql:
	python3 sql/run_sqlite_products.py

r:
	Rscript r/product_summary.R

julia:
	julia julia/product_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_product_registry_fingerprint.c -o outputs/fnv_product_registry_fingerprint
	./outputs/fnv_product_registry_fingerprint data/data_products.csv > outputs/fnv_product_registry_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/lineage_summary.cpp -o outputs/lineage_summary
	./outputs/lineage_summary

clean:
	find outputs -type f ! -name ".gitkeep" -delete
