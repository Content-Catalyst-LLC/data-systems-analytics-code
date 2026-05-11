CREATE TABLE IF NOT EXISTS pipeline_stages (
    stage_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    stage_type TEXT NOT NULL,
    mode TEXT NOT NULL,
    upstream_stage TEXT,
    downstream_stage TEXT,
    owner TEXT NOT NULL,
    criticality TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    run_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    run_mode TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT NOT NULL,
    input_rows INTEGER NOT NULL,
    output_rows INTEGER NOT NULL,
    failed_rows INTEGER NOT NULL,
    retry_count INTEGER NOT NULL,
    status TEXT NOT NULL,
    code_version TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quality_gates (
    gate_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    dimension TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    threshold REAL NOT NULL,
    observed_value REAL NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS observability_metrics (
    metric_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    throughput_rows_per_sec REAL NOT NULL,
    latency_seconds REAL NOT NULL,
    lag_seconds REAL NOT NULL,
    error_rate REAL NOT NULL,
    watermark_lag_seconds REAL NOT NULL,
    backpressure_ms REAL NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lineage_edges (
    edge_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    from_node TEXT NOT NULL,
    to_node TEXT NOT NULL,
    edge_type TEXT NOT NULL,
    records_moved INTEGER NOT NULL,
    transformation_summary TEXT NOT NULL,
    lineage_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS backfill_requests (
    backfill_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    requested_at TEXT NOT NULL,
    reason TEXT NOT NULL,
    start_period TEXT NOT NULL,
    end_period TEXT NOT NULL,
    expected_rows INTEGER NOT NULL,
    status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS idempotency_checks (
    check_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    stage_name TEXT NOT NULL,
    key_strategy TEXT NOT NULL,
    rerun_input_rows INTEGER NOT NULL,
    first_output_rows INTEGER NOT NULL,
    second_output_rows INTEGER NOT NULL,
    duplicate_effect_count INTEGER NOT NULL,
    status TEXT NOT NULL
);
