.PHONY: python r sql clean

python:
	python3 python/data_lifecycle_retention_workflow.py

r:
	Rscript r/data_lifecycle_retention_audit.R

sql:
	sqlite3 outputs/lifecycle_demo.sqlite < sql/data_lifecycle_schema.sql

clean:
	rm -f outputs/*.csv outputs/*.json outputs/*.sqlite
