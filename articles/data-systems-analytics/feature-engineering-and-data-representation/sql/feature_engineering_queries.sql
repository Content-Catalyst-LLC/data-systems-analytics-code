-- 1. Feature inventory by family, status, and leakage risk.
SELECT
    feature_family,
    status,
    leakage_risk,
    COUNT(*) AS feature_count
FROM feature_registry
GROUP BY feature_family, status, leakage_risk
ORDER BY feature_family, status;

-- 2. Features with high or medium leakage risk.
SELECT
    feature_id,
    feature_name,
    feature_family,
    source_field,
    transformation,
    leakage_risk,
    status,
    owner
FROM feature_registry
WHERE leakage_risk IN ('medium', 'high')
ORDER BY leakage_risk DESC, feature_id;

-- 3. Transformation rules that violate training-only or prediction-time availability.
SELECT
    r.rule_id,
    f.feature_name,
    r.rule_type,
    r.fit_scope,
    r.applied_scope,
    r.requires_training_fit,
    r.allowed_at_prediction_time,
    r.review_status
FROM transformation_rules r
JOIN feature_registry f ON r.feature_id = f.feature_id
WHERE r.fit_scope NOT IN ('training_only', 'no_fit')
   OR r.allowed_at_prediction_time <> 'true'
   OR r.review_status <> 'approved'
ORDER BY f.feature_name;

-- 4. Feature quality checks requiring attention.
SELECT
    f.feature_name,
    c.check_type,
    c.status,
    c.severity,
    c.notes
FROM feature_quality_checks c
JOIN feature_registry f ON c.feature_id = f.feature_id
WHERE c.status <> 'pass'
ORDER BY c.severity DESC, f.feature_name;

-- 5. Blocked or watchlisted feature selection items.
SELECT
    f.feature_name,
    s.selection_method,
    s.score,
    s.selected,
    s.selection_status
FROM selection_scores s
JOIN feature_registry f ON s.feature_id = f.feature_id
WHERE s.selection_status NOT IN ('approved')
ORDER BY s.selection_status, s.score DESC;

-- 6. Representation sets with leakage, high sparsity, or low approval share.
SELECT
    representation_name,
    feature_count,
    sparsity_ratio,
    oov_rate,
    leakage_flag_count,
    approved_feature_share,
    status
FROM representation_metrics
WHERE leakage_flag_count > 0
   OR sparsity_ratio > 0.85
   OR approved_feature_share < 0.75
   OR status <> 'approved'
ORDER BY leakage_flag_count DESC, approved_feature_share ASC;
