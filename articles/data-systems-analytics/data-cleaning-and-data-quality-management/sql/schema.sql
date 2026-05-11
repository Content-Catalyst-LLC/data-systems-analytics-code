CREATE TABLE IF NOT EXISTS raw_customer_records (
    record_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    customer_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    country_code TEXT NOT NULL,
    status TEXT NOT NULL,
    signup_date TEXT NOT NULL,
    last_updated TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    lifetime_value REAL
);

CREATE TABLE IF NOT EXISTS quality_rules (
    rule_id TEXT PRIMARY KEY,
    dimension TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    field_name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    threshold REAL NOT NULL,
    severity TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS status_mapping (
    source_system TEXT NOT NULL,
    source_value TEXT NOT NULL,
    canonical_value TEXT NOT NULL,
    mapping_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS root_cause_register (
    issue_id TEXT PRIMARY KEY,
    quality_dimension TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    affected_system TEXT NOT NULL,
    root_cause TEXT NOT NULL,
    process_owner TEXT NOT NULL,
    impact_level TEXT NOT NULL,
    remediation_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_incidents (
    incident_id TEXT PRIMARY KEY,
    detected_at TEXT NOT NULL,
    dataset TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    failed_records INTEGER NOT NULL,
    affected_metric TEXT NOT NULL,
    incident_status TEXT NOT NULL,
    steward_notes TEXT NOT NULL
);
