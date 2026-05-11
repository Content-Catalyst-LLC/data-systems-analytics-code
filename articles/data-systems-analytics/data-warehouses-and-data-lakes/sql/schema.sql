CREATE TABLE IF NOT EXISTS data_assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    architecture_zone TEXT NOT NULL,
    storage_form TEXT NOT NULL,
    schema_strategy TEXT NOT NULL,
    file_or_table_format TEXT NOT NULL,
    owner TEXT NOT NULL,
    governance_status TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    size_gb REAL NOT NULL,
    freshness_hours REAL NOT NULL,
    pii_classification TEXT NOT NULL,
    query_frequency_per_day REAL NOT NULL,
    ml_ready INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dimensional_model_tables (
    table_id TEXT PRIMARY KEY,
    table_name TEXT NOT NULL,
    model_role TEXT NOT NULL,
    grain TEXT NOT NULL,
    business_process TEXT NOT NULL,
    conformed_dimension INTEGER NOT NULL,
    slowly_changing_type TEXT NOT NULL,
    primary_key TEXT NOT NULL,
    foreign_keys TEXT,
    owner TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lake_zones (
    zone_id TEXT PRIMARY KEY,
    zone_name TEXT NOT NULL,
    purpose TEXT NOT NULL,
    allowed_formats TEXT NOT NULL,
    metadata_required INTEGER NOT NULL,
    quality_gate_required INTEGER NOT NULL,
    retention_days INTEGER NOT NULL,
    access_model TEXT NOT NULL,
    swamp_risk TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_controls (
    control_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    metadata_coverage REAL NOT NULL,
    lineage_coverage REAL NOT NULL,
    owner_assigned INTEGER NOT NULL,
    classification_applied INTEGER NOT NULL,
    quality_status TEXT NOT NULL,
    access_policy_status TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cost_performance_metrics (
    metric_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    monthly_storage_cost_usd REAL NOT NULL,
    monthly_compute_cost_usd REAL NOT NULL,
    mean_query_latency_seconds REAL NOT NULL,
    p95_query_latency_seconds REAL NOT NULL,
    compression_ratio REAL NOT NULL,
    cache_hit_rate REAL NOT NULL,
    scan_efficiency_score REAL NOT NULL,
    cost_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lakehouse_table_features (
    table_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    open_table_format TEXT NOT NULL,
    acid_transactions INTEGER NOT NULL,
    schema_evolution INTEGER NOT NULL,
    time_travel INTEGER NOT NULL,
    partition_evolution INTEGER NOT NULL,
    batch_stream_unified INTEGER NOT NULL,
    metadata_scalability INTEGER NOT NULL,
    table_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workload_requirements (
    workload_id TEXT PRIMARY KEY,
    workload_name TEXT NOT NULL,
    primary_use_case TEXT NOT NULL,
    requires_low_latency_sql INTEGER NOT NULL,
    requires_raw_data_access INTEGER NOT NULL,
    requires_ml_features INTEGER NOT NULL,
    requires_strong_governance INTEGER NOT NULL,
    requires_open_format INTEGER NOT NULL,
    preferred_architecture TEXT NOT NULL
);
