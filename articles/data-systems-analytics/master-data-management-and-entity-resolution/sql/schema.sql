CREATE TABLE IF NOT EXISTS source_records (
    record_id TEXT PRIMARY KEY,
    source_system TEXT NOT NULL,
    domain TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    source_entity_id TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    country TEXT,
    postal_code TEXT,
    legal_identifier TEXT,
    local_identifier TEXT,
    record_status TEXT NOT NULL,
    updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS candidate_matches (
    candidate_id TEXT PRIMARY KEY,
    left_record_id TEXT NOT NULL,
    right_record_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    match_method TEXT NOT NULL,
    name_similarity REAL NOT NULL,
    address_similarity REAL NOT NULL,
    identifier_match TEXT NOT NULL,
    relationship_evidence REAL NOT NULL,
    match_score REAL NOT NULL,
    recommended_action TEXT NOT NULL,
    review_required TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS master_entities (
    master_entity_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    master_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    authoritative_view TEXT NOT NULL,
    lifecycle_status TEXT NOT NULL,
    steward TEXT NOT NULL,
    created_at_utc TEXT NOT NULL,
    last_reviewed_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entity_crosswalk (
    master_entity_id TEXT NOT NULL,
    source_system TEXT NOT NULL,
    source_entity_id TEXT NOT NULL,
    record_id TEXT NOT NULL,
    link_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    link_status TEXT NOT NULL,
    effective_from_utc TEXT NOT NULL,
    effective_to_utc TEXT
);

CREATE TABLE IF NOT EXISTS survivorship_rules (
    rule_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    attribute_name TEXT NOT NULL,
    authority_rule TEXT NOT NULL,
    primary_source TEXT NOT NULL,
    secondary_source TEXT,
    conflict_action TEXT NOT NULL,
    review_required TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS hierarchy_edges (
    edge_id TEXT PRIMARY KEY,
    parent_entity_id TEXT NOT NULL,
    child_entity_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    relationship_view TEXT NOT NULL,
    effective_from_utc TEXT NOT NULL,
    effective_to_utc TEXT,
    confidence REAL NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS stewardship_queue (
    review_id TEXT PRIMARY KEY,
    candidate_id TEXT,
    master_entity_id TEXT,
    review_type TEXT NOT NULL,
    priority TEXT NOT NULL,
    status TEXT NOT NULL,
    assigned_steward TEXT NOT NULL,
    risk_reason TEXT NOT NULL,
    created_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS external_identifiers (
    external_id_id TEXT PRIMARY KEY,
    master_entity_id TEXT NOT NULL,
    identifier_type TEXT NOT NULL,
    identifier_value TEXT NOT NULL,
    issuing_authority TEXT NOT NULL,
    verification_status TEXT NOT NULL,
    last_verified_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS privacy_identity_risk (
    risk_id TEXT PRIMARY KEY,
    master_entity_id TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    linked_record_count INTEGER NOT NULL,
    contains_personal_data TEXT NOT NULL,
    reidentification_risk TEXT NOT NULL,
    linkage_sensitivity TEXT NOT NULL,
    purpose_review_status TEXT NOT NULL,
    mitigation TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mdm_lineage_events (
    event_id TEXT PRIMARY KEY,
    event_time_utc TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    input_record_id TEXT NOT NULL,
    output_master_entity_id TEXT NOT NULL,
    agent TEXT NOT NULL,
    rule_or_model TEXT NOT NULL,
    provenance_note TEXT NOT NULL
);
