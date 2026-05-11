-- 1. Causal study inventory by design, estimand, status, and risk.
SELECT design_type, estimand, status, risk_level, COUNT(*) AS study_count
FROM causal_study_registry
GROUP BY design_type, estimand, status, risk_level
ORDER BY design_type, estimand;

-- 2. Assumption checks requiring review.
SELECT s.study_name, a.assumption, a.status, a.severity, a.evidence, a.remediation
FROM assumption_checks a
JOIN causal_study_registry s ON a.study_id = s.study_id
WHERE a.status <> 'pass'
ORDER BY a.severity DESC, s.study_name;

-- 3. Difference in means for experimental / observational unit data.
SELECT study_id, treatment, COUNT(*) AS n, AVG(outcome) AS mean_outcome
FROM experiment_units
GROUP BY study_id, treatment
ORDER BY study_id, treatment;

-- 4. Difference-in-differences means.
SELECT study_id, group_name, post, AVG(outcome) AS mean_outcome
FROM did_panel
GROUP BY study_id, group_name, post
ORDER BY study_id, group_name, post;

-- 5. Regression-discontinuity local window.
SELECT study_id, treatment, COUNT(*) AS n, AVG(outcome) AS mean_outcome
FROM rdd_units
WHERE ABS(running_variable - cutoff) <= 2
GROUP BY study_id, treatment
ORDER BY study_id, treatment;

-- 6. Designs with low evidentiary status.
SELECT study_name, design_type, estimand, status, risk_level
FROM causal_study_registry
WHERE status <> 'approved'
ORDER BY risk_level DESC, status;
