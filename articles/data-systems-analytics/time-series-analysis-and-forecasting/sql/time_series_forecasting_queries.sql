-- 1. Forecast model inventory by family, validation design, and status.
SELECT model_family, validation_design, status, risk_level, COUNT(*) AS model_count
FROM forecast_model_registry
GROUP BY model_family, validation_design, status, risk_level
ORDER BY model_family, validation_design;

-- 2. Backtest forecast error by model and horizon.
SELECT
    model_id,
    horizon,
    AVG(ABS(actual - forecast)) AS mae,
    SQRT(AVG((actual - forecast) * (actual - forecast))) AS rmse,
    AVG(CASE WHEN actual >= lower_80 AND actual <= upper_80 THEN 1.0 ELSE 0.0 END) AS interval_coverage_80
FROM backtest_windows
GROUP BY model_id, horizon
ORDER BY model_id, horizon;

-- 3. Diagnostic checks requiring review.
SELECT series_id, check_type, status, severity, evidence, remediation
FROM diagnostic_checks
WHERE status <> 'pass'
ORDER BY severity DESC, check_type;

-- 4. Forecast interval widths by horizon.
SELECT
    model_id,
    horizon,
    AVG(upper_80 - lower_80) AS mean_width_80,
    AVG(upper_95 - lower_95) AS mean_width_95,
    release_status
FROM forecast_horizons
GROUP BY model_id, horizon, release_status
ORDER BY model_id, horizon;

-- 5. Yearly mean level for trend inspection.
SELECT series_id, SUBSTR(date, 1, 4) AS year, AVG(value) AS mean_value
FROM monthly_demand
GROUP BY series_id, SUBSTR(date, 1, 4)
ORDER BY series_id, year;
