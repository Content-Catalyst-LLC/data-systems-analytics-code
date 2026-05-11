CREATE TABLE IF NOT EXISTS data_assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    classification TEXT NOT NULL,
    contains_personal_data TEXT NOT NULL,
    contains_direct_identifiers TEXT NOT NULL,
    sensitivity_score REAL NOT NULL,
    owner TEXT NOT NULL,
    retention_days INTEGER NOT NULL,
    control_surface TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_policies (
    policy_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    principal_type TEXT NOT NULL,
    principal TEXT NOT NULL,
    access_type TEXT NOT NULL,
    decision TEXT NOT NULL,
    condition TEXT NOT NULL,
    justification TEXT NOT NULL,
    review_frequency_days INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS entitlements (
    entitlement_id TEXT PRIMARY KEY,
    principal TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    access_type TEXT NOT NULL,
    granted_date TEXT NOT NULL,
    last_reviewed_date TEXT NOT NULL,
    status TEXT NOT NULL,
    temporary_exception TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS privacy_purposes (
    purpose_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    purpose TEXT NOT NULL,
    lawful_or_policy_basis TEXT NOT NULL,
    minimized_fields TEXT NOT NULL,
    retention_aligned TEXT NOT NULL,
    secondary_use_reviewed TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_events (
    event_id TEXT PRIMARY KEY,
    event_time_utc TEXT NOT NULL,
    principal TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    access_type TEXT NOT NULL,
    records_accessed INTEGER NOT NULL,
    decision TEXT NOT NULL,
    anomaly_flag TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS data_flows (
    flow_id TEXT PRIMARY KEY,
    source_asset TEXT NOT NULL,
    target_asset TEXT NOT NULL,
    flow_type TEXT NOT NULL,
    masking_applied TEXT NOT NULL,
    tokenization_applied TEXT NOT NULL,
    purpose TEXT NOT NULL,
    owner TEXT NOT NULL
);
