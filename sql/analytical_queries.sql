-- Metric summary by domain and system
SELECT * FROM v_metric_summary;

-- Warning records for review
SELECT *
FROM mart_system_metrics
WHERE quality_flag <> 'valid'
ORDER BY observed_at, system_id;

-- High-criticality systems
SELECT DISTINCT system_id, system_name, owner, refresh_frequency
FROM dim_systems
WHERE criticality = 'high';
