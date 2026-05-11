CREATE TABLE IF NOT EXISTS data_products (
    product_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    product_name TEXT NOT NULL,
    owner TEXT NOT NULL,
    consumer_group TEXT NOT NULL,
    criticality TEXT NOT NULL,
    freshness_sla_hours INTEGER NOT NULL,
    semantic_status TEXT NOT NULL,
    quality_score REAL NOT NULL,
    access_model TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS semantic_metrics (
    metric_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    definition TEXT NOT NULL,
    grain TEXT NOT NULL,
    calculation_owner TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_events (
    event_date TEXT NOT NULL,
    product_id TEXT NOT NULL,
    consumer_group TEXT NOT NULL,
    dashboard_views INTEGER NOT NULL,
    notebook_sessions INTEGER NOT NULL,
    api_calls INTEGER NOT NULL,
    ad_hoc_queries INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_checks (
    check_id TEXT PRIMARY KEY,
    product_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    threshold REAL NOT NULL,
    observed_value REAL NOT NULL,
    last_status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS product_lineage (
    product_id TEXT NOT NULL,
    upstream_source TEXT NOT NULL,
    transformation_model TEXT NOT NULL,
    semantic_asset TEXT NOT NULL,
    consumption_surface TEXT NOT NULL
);
