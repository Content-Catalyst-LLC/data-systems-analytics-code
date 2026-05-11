# Notebook guidance

Use notebooks to inspect relational evidence, not to hide official schema logic.

Recommended pattern:

1. Run `python/relational_sql_scorecard.py`.
2. Load `outputs/relational_sql_manifest_python.json`.
3. Inspect table readiness, constraints, query workload fit, transaction scores, access-control scores, and integrity incidents.
4. Run the SQLite example to inspect joins, aggregations, constraints, and foreign-key enforcement.
5. Preserve unresolved schema and governance risks before treating relational outputs as certified institutional state.
