-- 1. Model registry by layer and lifecycle status.
SELECT
    layer,
    lifecycle_status,
    COUNT(*) AS model_count
FROM model_registry
GROUP BY layer, lifecycle_status
ORDER BY layer, lifecycle_status;

-- 2. Metric certification by domain.
SELECT
    domain,
    certification_status,
    COUNT(*) AS metric_count
FROM semantic_metrics
GROUP BY domain, certification_status
ORDER BY domain, certification_status;

-- 3. Model test status.
SELECT
    m.model_id,
    m.model_name,
    COUNT(t.test_id) AS test_count,
    SUM(CASE WHEN t.status = 'pass' THEN 1 ELSE 0 END) AS passing_tests,
    SUM(CASE WHEN t.status = 'warn' THEN 1 ELSE 0 END) AS warning_tests,
    SUM(CASE WHEN t.status = 'fail' THEN 1 ELSE 0 END) AS failing_tests
FROM model_registry m
LEFT JOIN model_tests t ON m.model_id = t.model_id
GROUP BY m.model_id, m.model_name
ORDER BY failing_tests DESC, warning_tests DESC, m.model_id;

-- 4. Semantic definition drift requiring review.
SELECT
    metric_name,
    certified_metric_id,
    local_definition_count,
    highest_risk_surface,
    drift_status
FROM definition_drift
WHERE drift_status IN ('medium', 'high')
ORDER BY local_definition_count DESC;

-- 5. Metric usage by consumption surface.
SELECT
    u.metric_id,
    s.metric_name,
    u.consumption_surface,
    SUM(u.query_count) AS query_count,
    SUM(u.dashboard_views) AS dashboard_views,
    SUM(u.notebook_sessions) AS notebook_sessions
FROM metric_usage u
JOIN semantic_metrics s ON u.metric_id = s.metric_id
GROUP BY u.metric_id, s.metric_name, u.consumption_surface
ORDER BY dashboard_views DESC;
