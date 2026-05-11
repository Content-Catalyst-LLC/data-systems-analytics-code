# Notebook guidance

Use notebooks to inspect pipeline evidence, not to hide official pipeline logic.

Recommended pattern:

1. Run `python/pipeline_processing_scorecard.py`.
2. Load `outputs/pipeline_processing_manifest_python.json`.
3. Inspect DAG topology, stage scorecards, run health, quality gates, observability, lineage, backfills, and idempotency checks.
4. Compare batch, stream, backfill, and replay modes.
5. Preserve unresolved reliability and governance gaps before promoting downstream outputs.
