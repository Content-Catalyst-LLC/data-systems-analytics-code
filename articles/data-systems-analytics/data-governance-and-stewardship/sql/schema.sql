CREATE TABLE IF NOT EXISTS data_assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    classification TEXT NOT NULL,
    criticality TEXT NOT NULL,
    certification_status TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    last_reviewed_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stewardship_roles (
    role_id TEXT PRIMARY KEY,
    person_or_group TEXT NOT NULL,
    role_type TEXT NOT NULL,
    domain TEXT NOT NULL,
    responsibility_scope TEXT NOT NULL,
    decision_authority TEXT NOT NULL,
    backup_owner TEXT NOT NULL,
    active TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_rights (
    decision_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    decision_area TEXT NOT NULL,
    decision_type TEXT NOT NULL,
    approver_role TEXT NOT NULL,
    consulted_roles TEXT NOT NULL,
    escalation_path TEXT NOT NULL,
    service_level_days INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS policy_register (
    policy_id TEXT PRIMARY KEY,
    policy_name TEXT NOT NULL,
    policy_domain TEXT NOT NULL,
    policy_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    effective_date TEXT NOT NULL,
    review_cycle_days INTEGER NOT NULL,
    enforcement_status TEXT NOT NULL,
    linked_assets TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_issues (
    issue_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    issue_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_at_utc TEXT NOT NULL,
    assigned_steward TEXT NOT NULL,
    days_open INTEGER NOT NULL,
    consumer_notified TEXT NOT NULL,
    root_cause TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS access_reviews (
    access_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    requester_group TEXT NOT NULL,
    purpose TEXT NOT NULL,
    access_level TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    decision TEXT NOT NULL,
    approver_role TEXT NOT NULL,
    review_status TEXT NOT NULL,
    review_days INTEGER NOT NULL,
    expiry_days INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS lifecycle_controls (
    control_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    lifecycle_stage TEXT NOT NULL,
    control_type TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    next_review_due_utc TEXT NOT NULL,
    retention_rule TEXT NOT NULL,
    disposal_required TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS responsible_use_risks (
    risk_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    use_case TEXT NOT NULL,
    risk_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    review_status TEXT NOT NULL,
    mitigation TEXT NOT NULL,
    review_owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_events (
    event_id TEXT PRIMARY KEY,
    event_time_utc TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,
    decision_id TEXT,
    policy_id TEXT,
    outcome TEXT NOT NULL,
    notes TEXT NOT NULL
);
