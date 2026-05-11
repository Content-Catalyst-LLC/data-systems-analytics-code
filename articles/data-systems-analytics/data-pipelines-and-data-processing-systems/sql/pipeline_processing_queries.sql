-- 1. Pipeline topology by stage.
SELECT pipeline_name, stage_name, stage_type, mode, upstream_stage, downstream_stage, owner, criticality, status
FROM pipeline_stages
ORDER BY pipeline_name, stage_id;

-- 2. Run health summary.
SELECT pipeline_name, run_mode, status,
       COUNT(*) AS run_count,
       SUM(input_rows) AS input_rows,
       SUM(output_rows) AS output_rows,
       SUM(failed_rows) AS failed_rows,
       AVG(failed_rows * 1.0 / input_rows) AS mean_failure_rate,
       AVG(retry_count) AS mean_retries
FROM pipeline_runs
GROUP BY pipeline_name, run_mode, status
ORDER BY pipeline_name, run_mode;

-- 3. Quality gates requiring review.
SELECT pipeline_name, stage_name, dimension, rule_name, threshold, observed_value, severity, status
FROM quality_gates
WHERE status <> 'pass' OR observed_value < threshold
ORDER BY severity DESC, pipeline_name, stage_name;

-- 4. Observability warnings.
SELECT pipeline_name, observed_at, latency_seconds, lag_seconds, error_rate, watermark_lag_seconds, backpressure_ms, status
FROM observability_metrics
WHERE status <> 'pass' OR lag_seconds > 60 OR error_rate > 0.005 OR backpressure_ms > 100
ORDER BY observed_at;

-- 5. Partial lineage edges.
SELECT pipeline_name, from_node, to_node, edge_type, records_moved, lineage_status
FROM lineage_edges
WHERE lineage_status <> 'complete'
ORDER BY pipeline_name, edge_id;

-- 6. Idempotency checks requiring review.
SELECT pipeline_name, stage_name, key_strategy, first_output_rows, second_output_rows, duplicate_effect_count, status
FROM idempotency_checks
WHERE status <> 'pass' OR duplicate_effect_count > 0
ORDER BY pipeline_name, stage_name;
