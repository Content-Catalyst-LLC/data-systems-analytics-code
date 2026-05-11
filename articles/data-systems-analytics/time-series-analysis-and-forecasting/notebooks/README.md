# Notebook guidance

Use notebooks to inspect temporal evidence, not to hide official forecast release logic.

Recommended pattern:

1. Run `python/time_series_forecasting_scorecard.py`.
2. Load `outputs/time_series_forecasting_manifest_python.json`.
3. Inspect autocorrelation, year means, generated backtest errors, model scorecards, interval widths, and diagnostic checks.
4. Compare seasonal naive, moving average, regression, SARIMA, and legacy trend-line workflows.
5. Keep exploratory analysis separate from released forecast records.
