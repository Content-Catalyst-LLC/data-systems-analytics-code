# Notebook guidance

Use notebooks to inspect outputs, not to hide platform logic.

Recommended pattern:

1. Run `python/platform_scorecard.py`.
2. Load `outputs/platform_manifest_python.json`.
3. Inspect layer coverage, pipeline edges, and cost summary.
4. Compare architectural coverage against required layers.
5. Keep exploratory notes separate from promoted architecture checks.
