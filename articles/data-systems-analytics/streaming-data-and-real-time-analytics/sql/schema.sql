CREATE TABLE IF NOT EXISTS event_stream (
    event_id TEXT PRIMARY KEY,
    event_key TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_time TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    region TEXT NOT NULL,
    source_system TEXT NOT NULL,
    value REAL NOT NULL,
    quantity INTEGER NOT NULL,
    quality_score REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS stream_topic_registry (
    topic_id TEXT PRIMARY KEY,
    topic_name TEXT NOT NULL,
    event_domain TEXT NOT NULL,
    retention_hours INTEGER NOT NULL,
    partition_count INTEGER NOT NULL,
    replication_factor INTEGER NOT NULL,
    delivery_semantics TEXT NOT NULL,
    owner TEXT NOT NULL,
    status TEXT NOT NULL,
    risk_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS window_definitions (
    window_id TEXT PRIMARY KEY,
    stream_name TEXT NOT NULL,
    window_type TEXT NOT NULL,
    size_seconds INTEGER NOT NULL,
    slide_seconds INTEGER NOT NULL,
    allowed_lateness_seconds INTEGER NOT NULL,
    trigger_policy TEXT NOT NULL,
    output_mode TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS watermark_observations (
    observation_id TEXT PRIMARY KEY,
    stream_name TEXT NOT NULL,
    processing_time TEXT NOT NULL,
    observed_max_event_time TEXT NOT NULL,
    watermark_time TEXT NOT NULL,
    late_event_count INTEGER NOT NULL,
    state_size_mb REAL NOT NULL,
    backpressure_ms INTEGER NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_rules (
    rule_id TEXT PRIMARY KEY,
    rule_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    condition TEXT NOT NULL,
    threshold REAL NOT NULL,
    window_seconds INTEGER NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance_checks (
    check_id TEXT PRIMARY KEY,
    check_type TEXT NOT NULL,
    status TEXT NOT NULL,
    severity TEXT NOT NULL,
    evidence TEXT NOT NULL,
    remediation TEXT NOT NULL
);
