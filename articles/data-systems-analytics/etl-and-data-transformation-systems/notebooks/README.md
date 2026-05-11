# Notebook guidance

Use notebooks to inspect transformation evidence, not to hide official transformation logic.

Recommended pattern:

1. Run `python/etl_transformation_scorecard.py`.
2. Load `outputs/etl_transformation_manifest_python.json`.
3. Inspect canonical customers, canonical orders, rejected records, CDC operation summaries, lineage records, and test scorecards.
4. Compare raw extracts with canonical outputs.
5. Preserve mapping decisions and rejected-record reasons before publishing downstream state.
