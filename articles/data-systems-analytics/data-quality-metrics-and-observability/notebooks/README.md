# Notebook guidance

Use notebooks to inspect data quality and observability, not to hide production quality logic.

Recommended pattern:

1. Run `python/quality_observability_scorecard.py`.
2. Load `outputs/quality_observability_manifest_python.json`.
3. Inspect dataset reliability, trust risk, quality dimensions, incidents, and lineage impact.
4. Compare critical certified assets against reviewed, uncertified, and legacy assets.
5. Keep exploratory incident analysis separate from official quality rule definitions.
