.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/streaming_analytics_scorecard.py

sql:
	python3 sql/run_sqlite_streaming_analytics.py

r:
	Rscript r/streaming_analytics_summary.R

julia:
	julia julia/streaming_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_event_stream_fingerprint.c -o outputs/fnv_event_stream_fingerprint
	./outputs/fnv_event_stream_fingerprint data/event_stream.csv > outputs/fnv_event_stream_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/window_policy_adjacency.cpp -o outputs/window_policy_adjacency
	./outputs/window_policy_adjacency

quarto:
	quarto render quarto/streaming-analytics-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
