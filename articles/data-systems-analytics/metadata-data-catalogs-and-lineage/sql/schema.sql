CREATE TABLE IF NOT EXISTS data_assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    asset_type TEXT NOT NULL,
    owner TEXT NOT NULL,
    steward TEXT NOT NULL,
    classification TEXT NOT NULL,
    certification_status TEXT NOT NULL,
    criticality TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    last_reviewed_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS metadata_elements (
    metadata_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    metadata_type TEXT NOT NULL,
    element_name TEXT NOT NULL,
    value_present TEXT NOT NULL,
    quality_status TEXT NOT NULL,
    source TEXT NOT NULL,
    review_required TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS catalog_entries (
    catalog_entry_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    discoverable TEXT NOT NULL,
    description_complete TEXT NOT NULL,
    owner_visible TEXT NOT NULL,
    quality_visible TEXT NOT NULL,
    lineage_visible TEXT NOT NULL,
    policy_visible TEXT NOT NULL,
    usage_visible TEXT NOT NULL,
    trust_label TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS glossary_terms (
    term_id TEXT PRIMARY KEY,
    term_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    definition_status TEXT NOT NULL,
    linked_asset_id TEXT NOT NULL,
    semantic_owner TEXT NOT NULL,
    certification_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lineage_edges (
    edge_id TEXT PRIMARY KEY,
    upstream_asset TEXT NOT NULL,
    downstream_asset TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    lineage_granularity TEXT NOT NULL,
    impact_level TEXT NOT NULL,
    observed_by TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS provenance_events (
    event_id TEXT PRIMARY KEY,
    event_time_utc TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    prov_entity TEXT NOT NULL,
    prov_activity TEXT NOT NULL,
    prov_agent TEXT NOT NULL,
    version_id TEXT NOT NULL,
    provenance_complete TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS policy_tags (
    policy_tag_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    tag_type TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    policy_owner TEXT NOT NULL,
    enforcement_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_signals (
    signal_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    signal_name TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    observed_value REAL NOT NULL,
    expected_value REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS catalog_usage (
    usage_date TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    search_count INTEGER NOT NULL,
    view_count INTEGER NOT NULL,
    query_count INTEGER NOT NULL,
    downstream_consumer_count INTEGER NOT NULL,
    issue_comment_count INTEGER NOT NULL
);
