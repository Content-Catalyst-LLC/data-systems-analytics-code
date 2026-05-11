-- 1. Quality check status by dimension.
SELECT
    quality_dimension,
    status,
    severity,
    COUNT(*) AS check_count
FROM quality_checks
GROUP BY quality_dimension, status, severity
ORDER BY quality_dimension, severity DESC;

-- 2. Critical datasets with warnings or failures.
SELECT
    r.dataset_id,
    r.dataset_name,
    r.criticality,
    q.quality_dimension,
    q.check_name,
    q.status,
    q.severity,
    q.observed_value
FROM dataset_registry r
JOIN quality_checks q ON r.dataset_id = q.dataset_id
WHERE r.criticality = 'high'
  AND q.status <> 'pass'
ORDER BY q.severity DESC, r.dataset_id;

-- 3. Open or unresolved incidents.
SELECT
    i.incident_id,
    r.dataset_name,
    i.severity,
    i.status,
    i.root_cause_category,
    i.time_to_ack_hours,
    i.time_to_resolve_hours,
    i.consumer_notified
FROM incidents i
JOIN dataset_registry r ON i.dataset_id = r.dataset_id
WHERE i.status <> 'resolved'
ORDER BY i.severity DESC, i.opened_at_utc;

-- 4. Lineage-aware impact by dataset.
SELECT
    r.dataset_id,
    r.dataset_name,
    COUNT(l.edge_id) AS downstream_dependency_count,
    SUM(CASE WHEN l.impact_level = 'high' THEN 1 ELSE 0 END) AS high_impact_dependencies
FROM dataset_registry r
LEFT JOIN lineage_impact l ON r.dataset_id = l.upstream_dataset
GROUP BY r.dataset_id, r.dataset_name
ORDER BY high_impact_dependencies DESC, downstream_dependency_count DESC;

-- 5. Observability alerts linked to incidents.
SELECT
    e.event_id,
    e.event_time_utc,
    e.dataset_id,
    e.event_type,
    e.signal_name,
    e.observed_value,
    e.baseline_value,
    e.alert_status,
    e.incident_id
FROM observability_events e
WHERE e.alert_status IN ('warn', 'triggered')
ORDER BY e.event_time_utc;
