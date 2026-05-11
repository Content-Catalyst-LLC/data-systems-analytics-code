-- 1. Data assets by classification and personal-data status.
SELECT
    classification,
    contains_personal_data,
    COUNT(*) AS asset_count,
    ROUND(AVG(sensitivity_score), 3) AS average_sensitivity
FROM data_assets
GROUP BY classification, contains_personal_data
ORDER BY average_sensitivity DESC;

-- 2. Allowed access policies for restricted or secret assets.
SELECT
    p.policy_id,
    a.asset_name,
    a.classification,
    p.principal,
    p.access_type,
    p.condition,
    p.review_frequency_days
FROM access_policies p
JOIN data_assets a ON p.asset_id = a.asset_id
WHERE p.decision = 'allow'
  AND a.classification IN ('restricted', 'secret')
ORDER BY a.classification DESC, p.principal;

-- 3. Stale or temporary entitlements needing review.
SELECT
    e.entitlement_id,
    e.principal,
    a.asset_name,
    a.classification,
    e.access_type,
    e.status,
    e.temporary_exception,
    e.last_reviewed_date
FROM entitlements e
JOIN data_assets a ON e.asset_id = a.asset_id
WHERE e.status <> 'active'
   OR e.temporary_exception = 'true'
ORDER BY e.status, e.last_reviewed_date;

-- 4. Privacy purposes requiring review.
SELECT
    p.purpose_id,
    a.asset_name,
    p.purpose,
    p.minimized_fields,
    p.retention_aligned,
    p.secondary_use_reviewed,
    p.status
FROM privacy_purposes p
JOIN data_assets a ON p.asset_id = a.asset_id
WHERE p.status <> 'approved'
   OR p.minimized_fields <> 'true'
   OR p.secondary_use_reviewed <> 'true'
ORDER BY p.status, a.asset_name;

-- 5. Audit anomalies.
SELECT
    event_id,
    event_time_utc,
    principal,
    asset_id,
    access_type,
    records_accessed,
    decision,
    anomaly_flag
FROM audit_events
WHERE anomaly_flag = 'true'
ORDER BY event_time_utc;
