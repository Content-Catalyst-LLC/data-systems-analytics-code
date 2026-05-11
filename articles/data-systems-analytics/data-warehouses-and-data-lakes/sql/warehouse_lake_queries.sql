-- 1. Asset inventory by architectural zone.
SELECT architecture_zone, storage_form, schema_strategy, governance_status,
       COUNT(*) AS asset_count,
       SUM(row_count) AS total_rows,
       SUM(size_gb) AS total_size_gb,
       AVG(freshness_hours) AS mean_freshness_hours
FROM data_assets
GROUP BY architecture_zone, storage_form, schema_strategy, governance_status
ORDER BY architecture_zone, governance_status;

-- 2. Data-swamp warning assets.
SELECT a.asset_id, a.asset_name, a.architecture_zone,
       g.metadata_coverage, g.lineage_coverage, g.owner_assigned,
       g.access_policy_status, g.certification_status
FROM data_assets a
JOIN governance_controls g ON a.asset_id = g.asset_id
WHERE g.metadata_coverage < 0.60
   OR g.lineage_coverage < 0.50
   OR g.owner_assigned = 0
   OR g.access_policy_status IN ('missing', 'unknown')
ORDER BY g.metadata_coverage, g.lineage_coverage;

-- 3. Warehouse dimensional model readiness.
SELECT model_role, conformed_dimension, certification_status,
       COUNT(*) AS table_count
FROM dimensional_model_tables
GROUP BY model_role, conformed_dimension, certification_status
ORDER BY model_role, certification_status;

-- 4. Cost/performance review.
SELECT a.asset_name, a.architecture_zone, c.monthly_storage_cost_usd, c.monthly_compute_cost_usd,
       c.p95_query_latency_seconds, c.scan_efficiency_score, c.cost_status
FROM data_assets a
JOIN cost_performance_metrics c ON a.asset_id = c.asset_id
WHERE c.cost_status <> 'good' OR c.p95_query_latency_seconds > 60
ORDER BY c.cost_status, c.p95_query_latency_seconds DESC;

-- 5. Lakehouse table feature coverage.
SELECT a.asset_name, l.open_table_format, l.acid_transactions, l.schema_evolution,
       l.time_travel, l.partition_evolution, l.batch_stream_unified, l.metadata_scalability,
       l.table_status
FROM lakehouse_table_features l
JOIN data_assets a ON l.asset_id = a.asset_id
ORDER BY l.table_status, a.asset_name;

-- 6. Workload architecture fit.
SELECT workload_name, primary_use_case, requires_low_latency_sql, requires_raw_data_access,
       requires_ml_features, requires_strong_governance, requires_open_format, preferred_architecture
FROM workload_requirements
ORDER BY primary_use_case, workload_name;
