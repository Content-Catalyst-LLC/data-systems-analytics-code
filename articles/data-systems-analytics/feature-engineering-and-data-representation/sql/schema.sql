CREATE TABLE IF NOT EXISTS feature_registry (
    feature_id TEXT PRIMARY KEY,
    feature_name TEXT NOT NULL,
    feature_family TEXT NOT NULL,
    source_field TEXT NOT NULL,
    transformation TEXT NOT NULL,
    model_stage TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    leakage_risk TEXT NOT NULL,
    interpretability TEXT NOT NULL,
    cardinality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS transformation_rules (
    rule_id TEXT PRIMARY KEY,
    feature_id TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    fit_scope TEXT NOT NULL,
    applied_scope TEXT NOT NULL,
    requires_training_fit TEXT NOT NULL,
    allowed_at_prediction_time TEXT NOT NULL,
    review_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feature_quality_checks (
    check_id TEXT PRIMARY KEY,
    feature_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS selection_scores (
    selection_id TEXT PRIMARY KEY,
    feature_id TEXT NOT NULL,
    selection_method TEXT NOT NULL,
    score REAL NOT NULL,
    selected TEXT NOT NULL,
    selection_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS representation_metrics (
    metric_id TEXT PRIMARY KEY,
    representation_name TEXT NOT NULL,
    feature_count INTEGER NOT NULL,
    density REAL NOT NULL,
    sparsity_ratio REAL NOT NULL,
    oov_rate REAL NOT NULL,
    leakage_flag_count INTEGER NOT NULL,
    approved_feature_share REAL NOT NULL,
    status TEXT NOT NULL
);
