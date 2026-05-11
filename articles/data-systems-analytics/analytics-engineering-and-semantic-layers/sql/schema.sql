CREATE TABLE IF NOT EXISTS model_registry (
    model_id TEXT PRIMARY KEY,
    model_name TEXT NOT NULL,
    layer TEXT NOT NULL,
    domain TEXT NOT NULL,
    grain TEXT NOT NULL,
    owner TEXT NOT NULL,
    materialization TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL,
    criticality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS semantic_metrics (
    metric_id TEXT PRIMARY KEY,
    metric_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    definition TEXT NOT NULL,
    base_model TEXT NOT NULL,
    grain TEXT NOT NULL,
    owner TEXT NOT NULL,
    certification_status TEXT NOT NULL,
    version REAL NOT NULL,
    decision_critical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS model_tests (
    test_id TEXT PRIMARY KEY,
    model_id TEXT NOT NULL,
    test_type TEXT NOT NULL,
    expected_value REAL NOT NULL,
    observed_value REAL NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS semantic_lineage (
    edge_id TEXT PRIMARY KEY,
    upstream_model TEXT NOT NULL,
    downstream_model TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    impact_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metric_usage (
    usage_date TEXT NOT NULL,
    metric_id TEXT NOT NULL,
    consumption_surface TEXT NOT NULL,
    consumer_group TEXT NOT NULL,
    query_count INTEGER NOT NULL,
    dashboard_views INTEGER NOT NULL,
    notebook_sessions INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS definition_drift (
    metric_name TEXT NOT NULL,
    certified_metric_id TEXT NOT NULL,
    local_definition_count INTEGER NOT NULL,
    highest_risk_surface TEXT NOT NULL,
    drift_status TEXT NOT NULL
);
