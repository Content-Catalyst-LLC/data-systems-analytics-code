-- 1. Customer status mapping summary.
SELECT c.source_system, m.canonical_value AS customer_status, COUNT(*) AS customer_count
FROM raw_customer_extract c
LEFT JOIN status_mapping m
  ON c.source_system = m.source_system
 AND c.status_code = m.source_value
 AND m.canonical_domain = 'customer_status'
GROUP BY c.source_system, m.canonical_value
ORDER BY c.source_system, customer_status;

-- 2. Order status and amount summary.
SELECT o.source_system, m.canonical_value AS order_status,
       COUNT(*) AS order_count,
       SUM(o.amount) AS total_amount,
       AVG(o.amount) AS mean_amount
FROM raw_order_extract o
LEFT JOIN status_mapping m
  ON o.source_system = m.source_system
 AND o.status_code = m.source_value
 AND m.canonical_domain = 'order_status'
GROUP BY o.source_system, m.canonical_value
ORDER BY o.source_system, order_status;

-- 3. Records requiring quality review.
SELECT 'customer' AS entity, source_system, source_customer_id AS source_id,
       CASE
         WHEN email IS NULL OR email = '' THEN 'missing_email'
         ELSE 'ok'
       END AS quality_status
FROM raw_customer_extract
WHERE email IS NULL OR email = ''
UNION ALL
SELECT 'order' AS entity, source_system, source_order_id AS source_id,
       'missing_customer_mapping' AS quality_status
FROM raw_order_extract
WHERE source_customer_id IN ('CRM-404');

-- 4. CDC operation counts.
SELECT entity, operation, COUNT(*) AS event_count, MIN(sequence_number) AS first_sequence, MAX(sequence_number) AS last_sequence
FROM cdc_events
GROUP BY entity, operation
ORDER BY entity, operation;

-- 5. Transformation tests requiring remediation.
SELECT scope, test_name, status, severity, condition
FROM transformation_tests
WHERE status <> 'pass'
ORDER BY severity DESC, scope, test_name;

-- 6. Orchestration run health.
SELECT pipeline_name,
       SUM(input_rows) AS input_rows,
       SUM(loaded_rows) AS loaded_rows,
       SUM(rejected_rows) AS rejected_rows,
       AVG(rejected_rows * 1.0 / input_rows) AS reject_rate,
       status
FROM orchestration_runs
GROUP BY pipeline_name, status
ORDER BY reject_rate DESC;
