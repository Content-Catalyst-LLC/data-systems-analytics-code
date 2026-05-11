CREATE TABLE IF NOT EXISTS source_systems (
    system_id TEXT PRIMARY KEY,
    system_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    system_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    primary_entity TEXT NOT NULL,
    identifier_field TEXT NOT NULL,
    refresh_pattern TEXT NOT NULL,
    sensitivity TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_mappings (
    mapping_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    target_model TEXT NOT NULL,
    source_field TEXT NOT NULL,
    target_field TEXT NOT NULL,
    transformation_type TEXT NOT NULL,
    semantic_risk TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entity_crosswalk (
    canonical_entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    crm_customer_id TEXT,
    erp_account_id TEXT,
    support_contact_id TEXT,
    facility_sensor_id TEXT,
    facility_reporting_id TEXT,
    match_method TEXT NOT NULL,
    confidence REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS interoperability_checks (
    check_id TEXT PRIMARY KEY,
    layer TEXT NOT NULL,
    check_name TEXT NOT NULL,
    expected_value REAL NOT NULL,
    observed_value REAL NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lineage_events (
    event_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    target_asset TEXT NOT NULL,
    job_name TEXT NOT NULL,
    run_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_time_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS message_payloads (
    payload_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    message_type TEXT NOT NULL,
    syntax_valid TEXT NOT NULL,
    semantic_valid TEXT NOT NULL,
    minimized_payload TEXT NOT NULL,
    consumer_ready TEXT NOT NULL
);
