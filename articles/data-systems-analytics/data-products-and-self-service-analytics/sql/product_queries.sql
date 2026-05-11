-- 1. Product registry by domain.
SELECT
    domain,
    COUNT(*) AS product_count,
    ROUND(AVG(quality_score), 3) AS average_quality_score
FROM data_products
GROUP BY domain
ORDER BY product_count DESC, domain;

-- 2. Certified metric coverage.
SELECT
    p.product_id,
    p.product_name,
    p.domain,
    SUM(CASE WHEN m.certification_status = 'certified' THEN 1 ELSE 0 END) AS certified_metrics,
    COUNT(m.metric_id) AS total_metrics
FROM data_products p
LEFT JOIN semantic_metrics m ON p.product_id = m.product_id
GROUP BY p.product_id, p.product_name, p.domain
ORDER BY certified_metrics DESC;

-- 3. Quality check status by product.
SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN q.last_status = 'pass' THEN 1 ELSE 0 END) AS passing_checks,
    SUM(CASE WHEN q.last_status = 'warn' THEN 1 ELSE 0 END) AS warning_checks,
    SUM(CASE WHEN q.last_status = 'fail' THEN 1 ELSE 0 END) AS failing_checks
FROM data_products p
LEFT JOIN quality_checks q ON p.product_id = q.product_id
GROUP BY p.product_id, p.product_name
ORDER BY failing_checks DESC, warning_checks DESC, p.product_id;

-- 4. Self-service usage by product.
SELECT
    product_id,
    SUM(dashboard_views) AS dashboard_views,
    SUM(notebook_sessions) AS notebook_sessions,
    SUM(api_calls) AS api_calls,
    SUM(ad_hoc_queries) AS ad_hoc_queries,
    SUM(dashboard_views + notebook_sessions + api_calls + ad_hoc_queries) AS total_usage
FROM access_events
GROUP BY product_id
ORDER BY total_usage DESC;

-- 5. Products that should be reviewed.
SELECT
    product_id,
    product_name,
    semantic_status,
    quality_score,
    lifecycle_status
FROM data_products
WHERE semantic_status <> 'certified'
   OR quality_score < 0.90
   OR lifecycle_status IN ('beta', 'deprecated')
ORDER BY lifecycle_status, quality_score ASC;
