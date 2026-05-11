# Notebook guidance

Use notebooks to inspect interoperability scorecards, not to hide mapping logic.

Recommended pattern:

1. Run `python/interoperability_scorecard.py`.
2. Load `outputs/interoperability_manifest_python.json`.
3. Inspect mapping risk, entity crosswalk confidence, payload readiness, and check status by interoperability layer.
4. Compare technical success with semantic and organizational readiness.
5. Keep exploratory analysis separate from promoted mapping and contract logic.
