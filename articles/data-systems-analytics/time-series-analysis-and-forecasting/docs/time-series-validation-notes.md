# Time-series validation notes

Do not use ordinary random cross-validation for time-ordered forecasting problems.

Use:

- holdout periods
- expanding-window rolling origin
- sliding-window rolling origin
- horizon-specific evaluation
- backtesting by regime
- residual diagnostics
- forecast monitoring after release

The core rule is simple: evaluate the model using only information that would have been available at the forecast origin.
