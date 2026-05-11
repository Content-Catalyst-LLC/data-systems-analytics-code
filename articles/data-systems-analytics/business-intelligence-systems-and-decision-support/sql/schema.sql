CREATE TABLE IF NOT EXISTS bi_metrics (
    metric_id TEXT PRIMARY KEY,
    metric_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    owner TEXT NOT NULL,
    semantic_status TEXT NOT NULL,
    quality_score REAL NOT NULL,
    freshness_hours INTEGER NOT NULL,
    uncertainty_visible TEXT NOT NULL,
    decision_critical TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dashboard_inventory (
    dashboard_id TEXT PRIMARY KEY,
    dashboard_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    primary_user TEXT NOT NULL,
    decision_function TEXT NOT NULL,
    certification_status TEXT NOT NULL,
    refresh_sla_hours INTEGER NOT NULL,
    owner TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_thresholds (
    threshold_id TEXT PRIMARY KEY,
    metric_id TEXT NOT NULL,
    condition TEXT NOT NULL,
    threshold_value REAL NOT NULL,
    decision_owner TEXT NOT NULL,
    escalation_path TEXT NOT NULL,
    response_window_hours INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_events (
    event_date TEXT NOT NULL,
    threshold_id TEXT NOT NULL,
    metric_id TEXT NOT NULL,
    dashboard_id TEXT NOT NULL,
    observed_value REAL NOT NULL,
    alert_status TEXT NOT NULL,
    time_to_acknowledge_hours REAL NOT NULL,
    resolution_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS decision_reviews (
    review_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    decision_meeting TEXT NOT NULL,
    decision_taken TEXT NOT NULL,
    evidence_quality TEXT NOT NULL,
    action_traceable TEXT NOT NULL,
    followup_required TEXT NOT NULL
);
