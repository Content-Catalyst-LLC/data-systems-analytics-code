# Notebook guidance

Use notebooks to inspect causal evidence, not to hide the official design logic.

Recommended pattern:

1. Run `python/causal_inference_scorecard.py`.
2. Load `outputs/causal_inference_manifest_python.json`.
3. Inspect causal readiness scores, effect estimates, assumptions, and design-type summaries.
4. Compare randomized, difference-in-differences, regression-discontinuity, target-trial, and observational examples.
5. Keep exploratory analysis separate from final causal claims.
