-- 1. Model inventory by task, status, and risk.
SELECT
    task_type,
    status,
    risk_level,
    COUNT(*) AS model_count
FROM model_registry
GROUP BY task_type, status, risk_level
ORDER BY task_type, status;

-- 2. Threshold policies requiring review.
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

-- 3. Metric scorecard items outside or near limits.
SELECT
    m.model_name,
    s.metric_name,
    s.metric_family,
    s.target_question,
    s.acceptable_limit,
    s.observed_value,
    s.status
FROM metric_scorecard s
JOIN model_registry m ON s.model_id = m.model_id
WHERE s.status <> 'approved'
ORDER BY m.model_name, s.metric_family, s.metric_name;

-- 4. Binary prediction prevalence by model and subgroup.
SELECT
    model_id,
    subgroup,
    COUNT(*) AS n,
    AVG(y_true) AS observed_positive_rate,
    AVG(y_score) AS mean_score
FROM binary_predictions
GROUP BY model_id, subgroup
ORDER BY model_id, subgroup;

-- 5. Regression errors by segment.
SELECT
    model_id,
    segment,
    COUNT(*) AS n,
    AVG(ABS(y_pred - y_true)) AS mae,
    AVG((y_pred - y_true) * (y_pred - y_true)) AS mse,
    AVG(y_pred - y_true) AS bias
FROM regression_predictions
GROUP BY model_id, segment
ORDER BY model_id, segment;

-- 6. Monitoring windows requiring escalation.
SELECT
    m.model_name,
    w.window_start,
    w.window_end,
    w.roc_auc,
    w.brier_score,
    w.precision,
    w.recall,
    w.mae,
    w.drift_index,
    w.status
FROM monitoring_windows w
JOIN model_registry m ON w.model_id = m.model_id
WHERE w.status <> 'approved'
   OR w.drift_index >= 0.18
ORDER BY m.model_name, w.window_start;
