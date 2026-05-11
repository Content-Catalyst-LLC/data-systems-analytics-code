-- 1. Certified dashboard coverage by domain.
SELECT
    domain,
    COUNT(*) AS dashboard_count,
    SUM(CASE WHEN certification_status = 'certified' THEN 1 ELSE 0 END) AS certified_dashboards
FROM dashboard_inventory
GROUP BY domain
ORDER BY domain;

-- 2. Metric trust inputs by domain.
SELECT
    domain,
    COUNT(*) AS metric_count,
    ROUND(AVG(quality_score), 3) AS average_quality_score,
    SUM(CASE WHEN semantic_status = 'certified' THEN 1 ELSE 0 END) AS certified_metrics,
    SUM(CASE WHEN uncertainty_visible = 'true' THEN 1 ELSE 0 END) AS uncertainty_visible_metrics
FROM bi_metrics
GROUP BY domain
ORDER BY domain;

-- 3. Alert response performance.
SELECT
    d.dashboard_id,
    d.dashboard_name,
    ROUND(AVG(a.time_to_acknowledge_hours), 2) AS average_acknowledgement_hours,
    COUNT(a.threshold_id) AS alert_count
FROM dashboard_inventory d
LEFT JOIN alert_events a ON d.dashboard_id = a.dashboard_id
GROUP BY d.dashboard_id, d.dashboard_name
ORDER BY average_acknowledgement_hours DESC;

-- 4. Decision traceability.
SELECT
    d.dashboard_id,
    d.dashboard_name,
    COUNT(r.review_id) AS review_count,
    SUM(CASE WHEN r.action_traceable = 'true' THEN 1 ELSE 0 END) AS traceable_actions
FROM dashboard_inventory d
LEFT JOIN decision_reviews r ON d.dashboard_id = r.dashboard_id
GROUP BY d.dashboard_id, d.dashboard_name
ORDER BY traceable_actions DESC;

-- 5. Dashboards requiring governance review.
SELECT
    dashboard_id,
    dashboard_name,
    certification_status,
    lifecycle_status,
    refresh_sla_hours
FROM dashboard_inventory
WHERE certification_status <> 'certified'
   OR lifecycle_status <> 'active'
   OR refresh_sla_hours > 48
ORDER BY lifecycle_status, certification_status;
