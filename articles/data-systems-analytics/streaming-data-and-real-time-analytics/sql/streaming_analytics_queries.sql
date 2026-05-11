-- 1. Event counts by type, region, and source.
SELECT event_type, region, source_system, COUNT(*) AS event_count, AVG(value) AS mean_value
FROM event_stream
GROUP BY event_type, region, source_system
ORDER BY event_type, region, source_system;

-- 2. Event-time tumbling minute windows.
SELECT
    STRFTIME('%Y-%m-%dT%H:%M:00Z', event_time) AS event_minute,
    event_type,
    COUNT(*) AS event_count,
    SUM(value) AS value_sum,
    AVG(value) AS mean_value
FROM event_stream
GROUP BY STRFTIME('%Y-%m-%dT%H:%M:00Z', event_time), event_type
ORDER BY event_minute, event_type;

-- 3. Lateness profile using processing-time minus event-time.
SELECT
    event_type,
    source_system,
    COUNT(*) AS event_count,
    AVG((JULIANDAY(processing_time) - JULIANDAY(event_time)) * 86400.0) AS mean_lateness_seconds,
    MAX((JULIANDAY(processing_time) - JULIANDAY(event_time)) * 86400.0) AS max_lateness_seconds
FROM event_stream
GROUP BY event_type, source_system
ORDER BY max_lateness_seconds DESC;

-- 4. Watermark and backpressure observations requiring review.
SELECT stream_name, processing_time, late_event_count, state_size_mb, backpressure_ms, status
FROM watermark_observations
WHERE status <> 'pass'
ORDER BY processing_time;

-- 5. Topic readiness risks.
SELECT topic_name, delivery_semantics, retention_hours, replication_factor, status, risk_level
FROM stream_topic_registry
WHERE status <> 'approved' OR delivery_semantics = 'at_most_once'
ORDER BY risk_level DESC, topic_name;

-- 6. Governance checks requiring remediation.
SELECT check_type, status, severity, evidence, remediation
FROM governance_checks
WHERE status <> 'pass'
ORDER BY severity DESC, check_type;
