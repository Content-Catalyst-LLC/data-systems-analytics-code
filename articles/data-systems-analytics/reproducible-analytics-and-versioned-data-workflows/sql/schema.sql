CREATE TABLE IF NOT EXISTS analytics_events (
    event_date TEXT NOT NULL,
    region TEXT NOT NULL,
    system TEXT NOT NULL,
    event_type TEXT NOT NULL,
    value INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS workflow_run_manifest (
    run_id TEXT PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    workflow_version TEXT NOT NULL,
    input_path TEXT NOT NULL,
    input_fingerprint TEXT,
    output_path TEXT,
    output_fingerprint TEXT,
    run_started_at_utc TEXT NOT NULL,
    git_commit TEXT,
    parameters_json TEXT
);
