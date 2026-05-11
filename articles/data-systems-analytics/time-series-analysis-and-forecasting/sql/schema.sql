CREATE TABLE IF NOT EXISTS monthly_demand (
    date TEXT PRIMARY KEY,
    series_id TEXT NOT NULL,
    value REAL NOT NULL,
    temperature_index REAL NOT NULL,
    promotion_index REAL NOT NULL,
    holiday_flag INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS forecast_model_registry (
    model_id TEXT PRIMARY KEY,
    series_id TEXT NOT NULL,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    frequency TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    uses_exogenous TEXT NOT NULL,
    validation_design TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS backtest_windows (
    window_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    series_id TEXT NOT NULL,
    origin_date TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    actual REAL NOT NULL,
    forecast REAL NOT NULL,
    lower_80 REAL NOT NULL,
    upper_80 REAL NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS diagnostic_checks (
    check_id TEXT PRIMARY KEY,
    series_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS forecast_horizons (
    forecast_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    series_id TEXT NOT NULL,
    origin_date TEXT NOT NULL,
    horizon INTEGER NOT NULL,
    forecast REAL NOT NULL,
    lower_80 REAL NOT NULL,
    upper_80 REAL NOT NULL,
    lower_95 REAL NOT NULL,
    upper_95 REAL NOT NULL,
    release_status TEXT NOT NULL
);
