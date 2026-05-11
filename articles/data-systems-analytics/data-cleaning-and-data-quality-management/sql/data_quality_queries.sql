-- 1. Overall quality profile.
SELECT
    COUNT(*) AS row_count,
    SUM(CASE WHEN email IS NOT NULL AND email <> '' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS email_completeness,
    SUM(CASE WHEN lifetime_value >= 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS nonnegative_value_rate,
    SUM(CASE WHEN country_code IN ('US', 'USA') THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS country_validity_rate
FROM raw_customer_records;

-- 2. Duplicate normalized e-mail clusters.
SELECT LOWER(TRIM(email)) AS normalized_email, COUNT(*) AS record_count
FROM raw_customer_records
WHERE email IS NOT NULL AND email <> ''
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY record_count DESC;

-- 3. Source-system quality symptoms.
SELECT source_system,
       COUNT(*) AS records,
       SUM(CASE WHEN email IS NULL OR email = '' THEN 1 ELSE 0 END) AS missing_email_count,
       SUM(CASE WHEN lifetime_value < 0 THEN 1 ELSE 0 END) AS negative_value_count
FROM raw_customer_records
GROUP BY source_system
ORDER BY source_system;

-- 4. Rules by dimension and severity.
SELECT dimension, severity, status, COUNT(*) AS rule_count
FROM quality_rules
GROUP BY dimension, severity, status
ORDER BY dimension, severity;

-- 5. Open quality incidents.
SELECT i.incident_id, r.dimension, r.rule_name, i.failed_records, i.affected_metric, i.incident_status, i.steward_notes
FROM quality_incidents i
JOIN quality_rules r ON i.rule_id = r.rule_id
WHERE i.incident_status <> 'closed'
ORDER BY r.severity DESC, i.detected_at;

-- 6. Root-cause register by owner and status.
SELECT process_owner, quality_dimension, remediation_status, COUNT(*) AS issue_count
FROM root_cause_register
GROUP BY process_owner, quality_dimension, remediation_status
ORDER BY process_owner, quality_dimension;
