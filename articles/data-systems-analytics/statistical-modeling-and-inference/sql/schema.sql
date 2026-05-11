CREATE TABLE IF NOT EXISTS sample_observations (
    observation_id TEXT PRIMARY KEY,
    group_id TEXT NOT NULL,
    outcome REAL NOT NULL,
    predictor_x REAL NOT NULL,
    predictor_z REAL NOT NULL,
    weight REAL NOT NULL,
    measurement_batch TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    model_family TEXT NOT NULL,
    estimand TEXT NOT NULL,
    outcome TEXT NOT NULL,
    predictors TEXT NOT NULL,
    assumption_profile TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS inference_claims (
    claim_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    claim_text TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    effect_size REAL NOT NULL,
    standard_error REAL NOT NULL,
    p_value REAL NOT NULL,
    confidence_low REAL NOT NULL,
    confidence_high REAL NOT NULL,
    practical_threshold REAL NOT NULL,
    claim_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS diagnostic_checks (
    check_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS robustness_checks (
    robustness_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    check_name TEXT NOT NULL,
    primary_estimate REAL NOT NULL,
    alternative_estimate REAL NOT NULL,
    absolute_change REAL NOT NULL,
    status TEXT NOT NULL,
    notes TEXT NOT NULL
);
