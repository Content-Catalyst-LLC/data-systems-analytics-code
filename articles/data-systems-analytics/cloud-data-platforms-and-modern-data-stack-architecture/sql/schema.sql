CREATE TABLE IF NOT EXISTS stack_components (
    component_id TEXT PRIMARY KEY,
    layer TEXT NOT NULL,
    component_name TEXT NOT NULL,
    owner TEXT NOT NULL,
    criticality TEXT NOT NULL,
    governance_control TEXT,
    observability_control TEXT
);

CREATE TABLE IF NOT EXISTS pipeline_catalog (
    pipeline_id TEXT PRIMARY KEY,
    source_layer TEXT NOT NULL,
    target_layer TEXT NOT NULL,
    latency_pattern TEXT NOT NULL,
    expected_frequency TEXT NOT NULL,
    owner TEXT NOT NULL,
    quality_gate TEXT
);

CREATE TABLE IF NOT EXISTS access_policies (
    policy_id TEXT PRIMARY KEY,
    scope TEXT NOT NULL,
    principal_type TEXT NOT NULL,
    access_pattern TEXT NOT NULL,
    control_type TEXT NOT NULL,
    sensitivity TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cost_events (
    event_date TEXT NOT NULL,
    service_category TEXT NOT NULL,
    workload TEXT NOT NULL,
    compute_units REAL NOT NULL,
    storage_gb REAL NOT NULL,
    estimated_cost REAL NOT NULL
);
