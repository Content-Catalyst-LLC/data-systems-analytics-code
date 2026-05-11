CREATE TABLE IF NOT EXISTS model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    model_family TEXT NOT NULL,
    prediction_target TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    intended_use TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS classification_predictions (
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

CREATE TABLE IF NOT EXISTS training_validation_splits (
    split_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    split_strategy TEXT NOT NULL,
    train_count INTEGER NOT NULL,
    validation_count INTEGER NOT NULL,
    test_count INTEGER NOT NULL,
    stratified TEXT NOT NULL,
    time_ordered TEXT NOT NULL,
    group_aware TEXT NOT NULL,
    test_set_protected TEXT NOT NULL,
    status TEXT NOT NULL
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

CREATE TABLE IF NOT EXISTS leakage_shift_checks (
    check_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS monitoring_windows (
    window_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    window_start TEXT NOT NULL,
    window_end TEXT NOT NULL,
    production_metric TEXT NOT NULL,
    metric_value REAL NOT NULL,
    validation_reference REAL NOT NULL,
    drift_index REAL NOT NULL,
    status TEXT NOT NULL
);
