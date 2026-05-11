# Time Series Analysis and Forecasting

This companion code models forecasting as temporal-evidence infrastructure: observed series, trend/seasonality structure, lag dependence, stationarity checks, forecast horizons, prediction intervals, rolling-origin evaluation, forecast-error records, structural-break checks, and monitoring.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Forecasting is conditional projection under temporal dependence.

```text
time-indexed observations → diagnostics → decomposition / model choice
        → rolling-origin backtesting → forecast horizons + intervals
        → monitoring, drift review, and forecast governance
```

A mature forecasting workflow does not ask only whether a model fits the past. It asks whether the past structure is stable enough to support future projection, whether uncertainty grows honestly by horizon, and whether forecast errors are monitored after deployment.
