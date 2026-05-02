DELETE FROM data_quality_results;

INSERT INTO data_quality_results (check_name, check_status, failed_records)
SELECT
    'observation_metric_value_not_null',
    CASE WHEN COUNT(*) = 0 THEN 'pass' ELSE 'fail' END,
    COUNT(*)
FROM stg_observations
WHERE metric_value IS NULL;

INSERT INTO data_quality_results (check_name, check_status, failed_records)
SELECT
    'observation_system_id_valid',
    CASE WHEN COUNT(*) = 0 THEN 'pass' ELSE 'fail' END,
    COUNT(*)
FROM stg_observations o
LEFT JOIN dim_systems s ON o.system_id = s.system_id
WHERE s.system_id IS NULL;

INSERT INTO data_quality_results (check_name, check_status, failed_records)
SELECT
    'observation_quality_flag_allowed',
    CASE WHEN COUNT(*) = 0 THEN 'pass' ELSE 'fail' END,
    COUNT(*)
FROM stg_observations
WHERE quality_flag NOT IN ('valid', 'warning', 'invalid');

SELECT * FROM data_quality_results;
