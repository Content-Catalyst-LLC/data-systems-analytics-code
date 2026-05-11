CREATE TABLE IF NOT EXISTS visualization_inventory (
    visual_id TEXT PRIMARY KEY,
    visual_title TEXT NOT NULL,
    visualization_context TEXT NOT NULL,
    audience TEXT NOT NULL,
    primary_task TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    status TEXT NOT NULL,
    version TEXT NOT NULL,
    publication_surface TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    last_reviewed_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chart_assessments (
    chart_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    chart_type TEXT NOT NULL,
    analytical_task TEXT NOT NULL,
    chart_fit TEXT NOT NULL,
    comparison_supported TEXT NOT NULL,
    exact_values_needed TEXT NOT NULL,
    distribution_visible TEXT NOT NULL,
    trend_visible TEXT NOT NULL,
    relationship_visible TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS encoding_assessments (
    encoding_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    primary_encoding TEXT NOT NULL,
    scale_type TEXT NOT NULL,
    axis_baseline_appropriate TEXT NOT NULL,
    sorting_appropriate TEXT NOT NULL,
    label_quality TEXT NOT NULL,
    color_dependency TEXT NOT NULL,
    perceptual_accuracy TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS uncertainty_elements (
    uncertainty_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    uncertainty_type TEXT NOT NULL,
    visual_form TEXT NOT NULL,
    near_claim TEXT NOT NULL,
    materiality TEXT NOT NULL,
    statement_quality TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS annotation_elements (
    annotation_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    annotation_type TEXT NOT NULL,
    text_quality TEXT NOT NULL,
    evidence_linked TEXT NOT NULL,
    near_relevant_visual TEXT NOT NULL,
    emphasis_risk TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS accessibility_checks (
    check_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS evidence_links (
    link_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    source_asset TEXT NOT NULL,
    method_reference TEXT NOT NULL,
    traceability_status TEXT NOT NULL,
    review_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audience_contexts (
    context_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    audience_type TEXT NOT NULL,
    technical_depth_required TEXT NOT NULL,
    summary_required TEXT NOT NULL,
    method_reference_required TEXT NOT NULL,
    decision_record_required TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS review_checkpoints (
    review_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    review_type TEXT NOT NULL,
    review_owner TEXT NOT NULL,
    status TEXT NOT NULL,
    findings_count INTEGER NOT NULL,
    blocking_issues INTEGER NOT NULL,
    completed_at_utc TEXT
);

CREATE TABLE IF NOT EXISTS visual_outputs (
    output_id TEXT PRIMARY KEY,
    visual_id TEXT NOT NULL,
    output_format TEXT NOT NULL,
    versioned TEXT NOT NULL,
    archived TEXT NOT NULL,
    publication_channel TEXT NOT NULL,
    hash_recorded TEXT NOT NULL,
    access_level TEXT NOT NULL
);
