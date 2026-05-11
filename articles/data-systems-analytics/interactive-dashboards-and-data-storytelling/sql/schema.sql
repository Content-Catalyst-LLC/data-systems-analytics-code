CREATE TABLE IF NOT EXISTS dashboard_inventory (
    dashboard_id TEXT PRIMARY KEY,
    dashboard_title TEXT NOT NULL,
    dashboard_type TEXT NOT NULL,
    audience TEXT NOT NULL,
    primary_use TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    status TEXT NOT NULL,
    refresh_cadence TEXT NOT NULL,
    view_count INTEGER NOT NULL,
    filter_count INTEGER NOT NULL,
    created_at_utc TEXT NOT NULL,
    last_reviewed_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kpi_definitions (
    kpi_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    kpi_name TEXT NOT NULL,
    definition_status TEXT NOT NULL,
    baseline_present TEXT NOT NULL,
    target_present TEXT NOT NULL,
    trend_present TEXT NOT NULL,
    denominator_present TEXT NOT NULL,
    owner TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS filter_controls (
    filter_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    filter_name TEXT NOT NULL,
    filter_type TEXT NOT NULL,
    default_state_visible TEXT NOT NULL,
    reset_available TEXT NOT NULL,
    consumer_relevant TEXT NOT NULL,
    complexity_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS linked_views (
    view_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    view_name TEXT NOT NULL,
    visual_type TEXT NOT NULL,
    purpose TEXT NOT NULL,
    linked_to TEXT,
    progressive_disclosure TEXT NOT NULL,
    design_risk TEXT NOT NULL,
    caption_quality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS story_points (
    story_point_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    sequence_order INTEGER NOT NULL,
    story_title TEXT NOT NULL,
    story_function TEXT NOT NULL,
    claim_id TEXT NOT NULL,
    linked_view_id TEXT NOT NULL,
    user_action_expected TEXT NOT NULL,
    uncertainty_visible TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS annotations (
    annotation_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    view_id TEXT NOT NULL,
    annotation_type TEXT NOT NULL,
    text_quality TEXT NOT NULL,
    evidence_linked TEXT NOT NULL,
    near_relevant_visual TEXT NOT NULL,
    emphasis_risk TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS interaction_events (
    event_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    user_task TEXT NOT NULL,
    friction_level TEXT NOT NULL,
    error_risk TEXT NOT NULL,
    observed_count INTEGER NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accessibility_checks (
    check_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_checks (
    governance_id TEXT PRIMARY KEY,
    dashboard_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL,
    blocking_issue TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_links (
    link_id TEXT PRIMARY KEY,
    claim_id TEXT NOT NULL,
    dashboard_id TEXT NOT NULL,
    source_asset TEXT NOT NULL,
    method_reference TEXT NOT NULL,
    traceability_status TEXT NOT NULL,
    review_status TEXT NOT NULL
);
