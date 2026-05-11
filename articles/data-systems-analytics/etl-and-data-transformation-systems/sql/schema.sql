CREATE TABLE IF NOT EXISTS raw_customer_extract (
    source_system TEXT NOT NULL,
    source_customer_id TEXT NOT NULL,
    customer_name TEXT NOT NULL,
    status_code TEXT NOT NULL,
    country_code TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    email TEXT
);

CREATE TABLE IF NOT EXISTS raw_order_extract (
    source_system TEXT NOT NULL,
    source_order_id TEXT NOT NULL,
    source_customer_id TEXT NOT NULL,
    order_time TEXT NOT NULL,
    amount REAL NOT NULL,
    currency TEXT NOT NULL,
    status_code TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS status_mapping (
    source_system TEXT NOT NULL,
    source_field TEXT NOT NULL,
    source_value TEXT NOT NULL,
    canonical_domain TEXT NOT NULL,
    canonical_value TEXT NOT NULL,
    active_flag INTEGER NOT NULL,
    mapping_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cdc_events (
    event_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    entity TEXT NOT NULL,
    operation TEXT NOT NULL,
    business_key TEXT NOT NULL,
    event_time TEXT NOT NULL,
    sequence_number INTEGER NOT NULL,
    payload_status TEXT,
    payload_amount REAL
);

CREATE TABLE IF NOT EXISTS transformation_tests (
    test_id TEXT PRIMARY KEY,
    test_name TEXT NOT NULL,
    scope TEXT NOT NULL,
    condition TEXT NOT NULL,
    expected_result TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS orchestration_runs (
    run_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT NOT NULL,
    source_batch_id TEXT NOT NULL,
    code_version TEXT NOT NULL,
    input_rows INTEGER NOT NULL,
    loaded_rows INTEGER NOT NULL,
    rejected_rows INTEGER NOT NULL,
    status TEXT NOT NULL
);
