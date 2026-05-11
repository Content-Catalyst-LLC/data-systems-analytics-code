# Notebook guidance

Use notebooks to inspect representation integrity, not to hide official feature logic.

Recommended pattern:

1. Run `python/feature_engineering_scorecard.py`.
2. Load `outputs/feature_engineering_manifest_python.json`.
3. Inspect engineered features, feature integrity scores, representation readiness, leakage risk, transformation rules, and selection status.
4. Compare numerical, categorical, crossed, temporal, embedding, and leakage-candidate features.
5. Keep exploratory feature experiments separate from approved feature registries.
