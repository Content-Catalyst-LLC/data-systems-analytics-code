# Notebook guidance

Use notebooks to inspect warehouse/lake evidence, not to hide official architecture logic.

Recommended pattern:

1. Run `python/warehouse_lake_scorecard.py`.
2. Load `outputs/warehouse_lake_manifest_python.json`.
3. Inspect asset readiness, zone controls, dimensional model scorecards, workload fit, and estate summary.
4. Compare warehouse, lake, and lakehouse fit by workload.
5. Preserve governance gaps before treating outputs as certified analytical assets.
