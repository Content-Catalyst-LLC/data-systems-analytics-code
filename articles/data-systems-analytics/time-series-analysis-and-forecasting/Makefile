.PHONY: run python sql r julia go rust c cpp quarto clean

run:
	bash bash/run_all.sh

python:
	python3 python/time_series_forecasting_scorecard.py

sql:
	python3 sql/run_sqlite_time_series_forecasting.py

r:
	Rscript r/time_series_forecasting_summary.R

julia:
	julia julia/forecast_readiness_score.jl

go:
	cd go && go run .

rust:
	cd rust && cargo run

c:
	mkdir -p outputs
	cc c/fnv_time_series_fingerprint.c -o outputs/fnv_time_series_fingerprint
	./outputs/fnv_time_series_fingerprint data/monthly_demand.csv > outputs/fnv_time_series_fingerprint.txt

cpp:
	mkdir -p outputs
	c++ -std=c++17 cpp/forecast_horizon_adjacency.cpp -o outputs/forecast_horizon_adjacency
	./outputs/forecast_horizon_adjacency

quarto:
	quarto render quarto/time-series-forecasting-template.qmd --output-dir ../outputs

clean:
	find outputs -type f ! -name ".gitkeep" -delete
