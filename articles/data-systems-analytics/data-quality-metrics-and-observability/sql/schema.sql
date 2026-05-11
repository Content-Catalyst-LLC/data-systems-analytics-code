CREATE TABLE IF NOT EXISTS dataset_registry (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    owner TEXT NOT NULL,
    criticality TEXT NOT NULL,
    expected_freshness_hours INTEGER NOT NULL,
    expected_row_count_min INTEGER NOT NULL,
    expected_row_count_max INTEGER NOT NULL,
    certification_status TEXT NOT NULL,
    consumer_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_checks (
    check_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    quality_dimension TEXT NOT NULL,
    check_name TEXT NOT NULL,
    expected_value REAL NOT NULL,
    observed_value REAL NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observability_events (
    event_id TEXT PRIMARY KEY,
    event_time_utc TEXT NOT NULL,
    dataset_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    observed_value REAL NOT NULL,
    baseline_value REAL NOT NULL,
    alert_status TEXT NOT NULL,
    incident_id TEXT
);

CREATE TABLE IF NOT EXISTS baselines (
    baseline_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    baseline_type TEXT NOT NULL,
    expected_value REAL NOT NULL,
    tolerance REAL NOT NULL,
    window_days INTEGER NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS incidents (
    incident_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL,
    opened_at_utc TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    root_cause_category TEXT NOT NULL,
    time_to_ack_hours REAL NOT NULL,
    time_to_resolve_hours REAL NOT NULL,
    consumer_notified TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lineage_impact (
    edge_id TEXT PRIMARY KEY,
    upstream_dataset TEXT NOT NULL,
    downstream_asset TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    impact_level TEXT NOT NULL,
    owner TEXT NOT NULL
);
