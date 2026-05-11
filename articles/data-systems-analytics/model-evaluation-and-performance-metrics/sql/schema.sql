CREATE TABLE IF NOT EXISTS model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    prediction_target TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    training_window TEXT NOT NULL,
    validation_window TEXT NOT NULL,
    intended_use TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS binary_predictions (
    prediction_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    cohort TEXT NOT NULL,
    subgroup TEXT NOT NULL,
    y_true INTEGER NOT NULL,
    y_score REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS regression_predictions (
    prediction_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    cohort TEXT NOT NULL,
    segment TEXT NOT NULL,
    y_true REAL NOT NULL,
    y_pred REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS threshold_policies (
    policy_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    threshold REAL NOT NULL,
    policy_name TEXT NOT NULL,
    false_positive_cost REAL NOT NULL,
    false_negative_cost REAL NOT NULL,
    decision_owner TEXT NOT NULL,
    review_status TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metric_scorecard (
    metric_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_family TEXT NOT NULL,
    target_question TEXT NOT NULL,
    acceptable_limit REAL NOT NULL,
    observed_value REAL NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS monitoring_windows (
    window_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    roc_auc REAL,
    brier_score REAL,
    precision REAL,
    recall REAL,
    mae REAL,
    drift_index REAL NOT NULL,
    status TEXT NOT NULL
);
