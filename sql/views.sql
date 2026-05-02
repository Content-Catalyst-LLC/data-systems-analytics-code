CREATE VIEW IF NOT EXISTS v_article_roadmap AS
SELECT
    a.priority,
    a.status,
    d.domain_name,
    a.title,
    a.slug
FROM articles a
JOIN domains d ON a.domain_key = d.domain_key
ORDER BY a.priority ASC, d.priority ASC, a.title ASC;

CREATE VIEW IF NOT EXISTS mart_system_metrics AS
SELECT
    o.observation_id,
    o.observed_at,
    s.system_id,
    s.system_name,
    s.domain,
    s.criticality,
    s.owner,
    o.metric_name,
    o.metric_value,
    o.unit,
    o.source_system,
    o.quality_flag
FROM stg_observations o
JOIN dim_systems s ON o.system_id = s.system_id;

CREATE VIEW IF NOT EXISTS v_metric_summary AS
SELECT
    domain,
    system_name,
    metric_name,
    unit,
    COUNT(*) AS n_records,
    ROUND(AVG(metric_value), 4) AS avg_value,
    ROUND(MIN(metric_value), 4) AS min_value,
    ROUND(MAX(metric_value), 4) AS max_value
FROM mart_system_metrics
GROUP BY domain, system_name, metric_name, unit
ORDER BY domain, system_name, metric_name;
