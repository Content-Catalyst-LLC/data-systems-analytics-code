-- 1. Model inventory by family, estimand, status, and risk.
SELECT model_family, estimand, status, risk_level, COUNT(*) AS model_count
FROM model_registry
GROUP BY model_family, estimand, status, risk_level
ORDER BY model_family, estimand;

-- 2. Group-level sample means and sample sizes.
SELECT group_id, COUNT(*) AS n, AVG(outcome) AS mean_outcome
FROM sample_observations
GROUP BY group_id
ORDER BY group_id;

-- 3. Claims requiring review.
SELECT m.model_name, c.claim_type, c.effect_size, c.standard_error, c.p_value,
       c.confidence_low, c.confidence_high, c.practical_threshold, c.claim_status
FROM inference_claims c
JOIN model_registry m ON c.model_id = m.model_id
WHERE c.claim_status <> 'approved'
ORDER BY c.claim_status, m.model_name;

-- 4. Diagnostic checks requiring remediation.
SELECT m.model_name, d.check_type, d.status, d.severity, d.evidence, d.remediation
FROM diagnostic_checks d
JOIN model_registry m ON d.model_id = m.model_id
WHERE d.status <> 'pass'
ORDER BY d.severity DESC, m.model_name;

-- 5. Robustness checks with large estimate changes or failures.
SELECT m.model_name, r.check_name, r.primary_estimate, r.alternative_estimate,
       r.absolute_change, r.status, r.notes
FROM robustness_checks r
JOIN model_registry m ON r.model_id = m.model_id
WHERE r.status <> 'pass' OR r.absolute_change >= 0.25
ORDER BY r.status, r.absolute_change DESC;

-- 6. P-value threshold claims below practical effect thresholds.
SELECT claim_id, model_id, effect_size, p_value, practical_threshold, claim_status
FROM inference_claims
WHERE ABS(effect_size) < ABS(practical_threshold)
ORDER BY p_value;
