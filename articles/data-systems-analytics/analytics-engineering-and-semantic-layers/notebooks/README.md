# Notebook guidance

Use notebooks to inspect semantic trust and adoption, not to hide certified metric logic.

Recommended pattern:

1. Run `python/semantic_layer_scorecard.py`.
2. Load `outputs/semantic_layer_manifest_python.json`.
3. Inspect model readiness, semantic metric trust, definition drift, and metric usage.
4. Compare certified metrics against reviewed, uncertified, local, and legacy definitions.
5. Keep exploratory calculations separate from official semantic definitions.
