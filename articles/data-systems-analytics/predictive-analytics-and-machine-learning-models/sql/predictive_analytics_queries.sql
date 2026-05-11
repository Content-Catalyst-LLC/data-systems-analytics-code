-- 1. Predictive model inventory by task, model family, status, and risk.
SELECT
    task_type,
    model_family,
    status,
    risk_level,
    COUNT(*) AS model_count
FROM model_registry
GROUP BY task_type, model_family, status, risk_level
ORDER BY task_type, model_family;

-- 2. Split designs requiring review.
SELECT
    m.model_name,
    s.split_strategy,
    s.stratified,
    s.time_ordered,
    s.group_aware,
    s.test_set_protected,
    s.status
FROM training_validation_splits s
JOIN model_registry m ON s.model_id = m.model_id
WHERE s.test_set_protected <> 'true'
   OR s.status <> 'approved'
ORDER BY m.model_name;

-- 3. Metric scorecard items outside full approval.
SELECT
    m.model_name,
    c.metric_name,
    c.metric_family,
    c.target_question,
    c.acceptable_limit,
    c.observed_value,
    c.status
FROM metric_scorecard c
JOIN model_registry m ON c.model_id = m.model_id
WHERE c.status <> 'approved'
ORDER BY m.model_name, c.metric_family;

-- 4. Threshold policies requiring review.
SELECT
    m.model_name,
    t.policy_name,
    t.threshold,
    t.false_positive_cost,
    t.false_negative_cost,
    t.review_status,
    t.notes
FROM threshold_policies t
JOIN model_registry m ON t.model_id = m.model_id
WHERE t.review_status <> 'approved'
ORDER BY m.model_name, t.threshold;

-- 5. Leakage and shift checks requiring remediation.
SELECT
    m.model_name,
    l.check_type,
    l.status,
    l.severity,
    l.evidence,
    l.remediation
FROM leakage_shift_checks l
JOIN model_registry m ON l.model_id = m.model_id
WHERE l.status <> 'pass'
ORDER BY l.severity DESC, m.model_name;

-- 6. Monitoring windows requiring escalation or review.
SELECT
    m.model_name,
    w.window_start,
    w.window_end,
    w.production_metric,
    w.metric_value,
    w.validation_reference,
    w.drift_index,
    w.status
FROM monitoring_windows w
JOIN model_registry m ON w.model_id = m.model_id
WHERE w.status <> 'approved'
   OR w.drift_index >= 0.18
ORDER BY m.model_name, w.window_start;
