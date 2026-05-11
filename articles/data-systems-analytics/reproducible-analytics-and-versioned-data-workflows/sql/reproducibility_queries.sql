-- Example reproducibility queries.

-- 1. Analytical summary by system.
SELECT
    system,
    COUNT(*) AS records,
    SUM(value) AS total_value,
    ROUND(AVG(value), 2) AS average_value
FROM analytics_events
GROUP BY system
ORDER BY system;

-- 2. Version-aware run comparison.
SELECT
    workflow_name,
    workflow_version,
    COUNT(*) AS recorded_runs,
    MIN(run_started_at_utc) AS first_run_utc,
    MAX(run_started_at_utc) AS latest_run_utc
FROM workflow_run_manifest
GROUP BY workflow_name, workflow_version
ORDER BY latest_run_utc DESC;

-- 3. Output lineage lookup.
SELECT
    run_id,
    input_path,
    input_fingerprint,
    output_path,
    output_fingerprint,
    git_commit,
    parameters_json
FROM workflow_run_manifest
ORDER BY run_started_at_utc DESC;
