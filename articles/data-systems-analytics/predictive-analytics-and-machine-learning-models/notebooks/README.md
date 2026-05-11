# Notebook guidance

Use notebooks to inspect predictive modeling evidence, not to hide official governance logic.

Recommended pattern:

1. Run `python/predictive_model_scorecard.py`.
2. Load `outputs/predictive_model_manifest_python.json`.
3. Inspect predictive readiness, classification summaries, calibration bins, thresholds, subgroup behavior, regression errors, drift windows, and governance gaps.
4. Compare binary classification, regression, ranking, and legacy model cases.
5. Keep exploratory modeling separate from final evidence records.
