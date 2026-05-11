CREATE TABLE IF NOT EXISTS system_inventory (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    system_type TEXT NOT NULL,
    storage_model TEXT NOT NULL,
    primary_workload TEXT NOT NULL,
    owner TEXT NOT NULL,
    criticality TEXT NOT NULL,
    records_millions REAL NOT NULL,
    data_volume_gb REAL NOT NULL,
    availability_target REAL NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_assets (
    asset_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    asset_name TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    grain TEXT NOT NULL,
    primary_key TEXT NOT NULL,
    foreign_key_count INTEGER NOT NULL,
    constraint_count INTEGER NOT NULL,
    owner TEXT NOT NULL,
    classification TEXT NOT NULL,
    lineage_status TEXT NOT NULL,
    quality_status TEXT NOT NULL,
    access_status TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS workload_catalog (
    workload_id TEXT PRIMARY KEY,
    workload_name TEXT NOT NULL,
    workload_type TEXT NOT NULL,
    systems_used TEXT NOT NULL,
    latency_requirement_ms REAL NOT NULL,
    throughput_requirement_per_minute REAL NOT NULL,
    consistency_need TEXT NOT NULL,
    availability_need TEXT NOT NULL,
    governance_need TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_controls (
    control_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    metadata_coverage REAL NOT NULL,
    lineage_coverage REAL NOT NULL,
    owner_assigned INTEGER NOT NULL,
    classification_applied INTEGER NOT NULL,
    access_policy_status TEXT NOT NULL,
    backup_status TEXT NOT NULL,
    recovery_test_status TEXT NOT NULL,
    retention_policy_status TEXT NOT NULL,
    quality_gate_status TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recovery_plans (
    plan_id TEXT PRIMARY KEY,
    system_id TEXT NOT NULL,
    recovery_point_objective_minutes REAL NOT NULL,
    recovery_time_objective_minutes REAL NOT NULL,
    last_backup_age_minutes REAL NOT NULL,
    last_restore_test_days_ago REAL NOT NULL,
    replication_mode TEXT NOT NULL,
    failover_coverage TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS integration_lineage (
    edge_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    target_system TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    frequency TEXT NOT NULL,
    lineage_visibility TEXT NOT NULL,
    transformation_owner TEXT NOT NULL,
    quality_gate TEXT NOT NULL,
    contract_status TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS architecture_risks (
    risk_id TEXT PRIMARY KEY,
    risk_area TEXT NOT NULL,
    system_id TEXT NOT NULL,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    likelihood TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);
