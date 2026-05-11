-- 1. Overall descriptive summary for primary value.
SELECT
    COUNT(*) AS n,
    COUNT(value) AS non_missing_value_count,
    COUNT(*) - COUNT(value) AS missing_value_count,
    AVG(value) AS mean_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value
FROM exploration_dataset;

-- 2. Subgroup summary to reduce aggregation masking.
SELECT
    segment,
    region,
    COUNT(*) AS n,
    COUNT(value) AS non_missing_value_count,
    AVG(value) AS mean_value,
    MIN(value) AS min_value,
    MAX(value) AS max_value
FROM exploration_dataset
GROUP BY segment, region
ORDER BY segment, region;

-- 3. Missingness by subgroup.
SELECT
    segment,
    region,
    COUNT(*) AS n,
    SUM(missing_flag) AS missing_value_count,
    AVG(missing_flag) AS missing_value_rate
FROM exploration_dataset
GROUP BY segment, region
ORDER BY missing_value_rate DESC;

-- 4. Category frequencies.
SELECT category, COUNT(*) AS n, COUNT(*) * 1.0 / (SELECT COUNT(*) FROM exploration_dataset) AS share
FROM exploration_dataset
GROUP BY category
ORDER BY n DESC;

-- 5. Exploration checks requiring action.
SELECT check_type, status, severity, evidence, remediation
FROM exploration_checks
WHERE status <> 'pass'
ORDER BY severity DESC, check_type;

-- 6. Active EDA questions by priority and mode.
SELECT priority, analysis_mode, COUNT(*) AS question_count
FROM exploration_questions
WHERE status = 'active'
GROUP BY priority, analysis_mode
ORDER BY priority, analysis_mode;
