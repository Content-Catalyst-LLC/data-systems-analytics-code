# Notebook guidance

Use notebooks to inspect model evaluation evidence, not to hide official evaluation logic.

Recommended pattern:

1. Run `python/model_evaluation_scorecard.py`.
2. Load `outputs/model_evaluation_manifest_python.json`.
3. Inspect threshold metrics, ROC-AUC, average precision, calibration bins, subgroup metrics, regression error, scorecard limits, and monitoring flags.
4. Compare ranking, threshold, calibration, regression, and monitoring dimensions separately.
5. Keep exploratory evaluation separate from approved model-governance records.
