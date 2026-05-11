-- Data Lifecycle Management and Retention
-- SQL schema and lifecycle review queries.
-- Designed for SQLite demonstration; adapt date arithmetic for other engines.

DROP TABLE IF EXISTS data_assets;
DROP TABLE IF EXISTS retention_rules;
DROP TABLE IF EXISTS lifecycle_review;

CREATE TABLE data_assets (
    asset_id TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    system_name TEXT NOT NULL,
    owner TEXT,
    classification TEXT NOT NULL,
    retention_category TEXT NOT NULL,
    created_date TEXT NOT NULL,
    trigger_date TEXT NOT NULL,
    last_accessed_date TEXT NOT NULL,
    legal_hold INTEGER NOT NULL CHECK (legal_hold IN (0, 1)),
    archival_value TEXT NOT NULL CHECK (archival_value IN ('low', 'medium', 'high')),
    storage_gb REAL NOT NULL CHECK (storage_gb >= 0),
    downstream_dependencies INTEGER NOT NULL CHECK (downstream_dependencies >= 0)
);

CREATE TABLE retention_rules (
    retention_category TEXT PRIMARY KEY,
    retention_years INTEGER NOT NULL CHECK (retention_years >= 0),
    default_action TEXT NOT NULL,
    requires_archival_review INTEGER NOT NULL CHECK (requires_archival_review IN (0, 1))
);

INSERT INTO retention_rules VALUES
('customer_contact_data', 2, 'delete_or_anonymize', 0),
('financial_records', 7, 'retain_until_expired_then_dispose', 0),
('system_logs', 1, 'delete', 0),
('research_observational_data', 10, 'archive_review', 1),
('employee_records', 7, 'retain_until_expired_then_dispose', 0),
('ml_training_extract', 2, 'delete_or_regenerate_from_governed_source', 0),
('dashboard_extract', 1, 'delete_or_rebuild_from_certified_source', 0);

INSERT INTO data_assets VALUES
('crm_contacts_raw', 'CRM contacts raw export', 'cloud_object_storage', 'sales_ops', 'personal_data', 'customer_contact_data', '2022-02-01', '2025-12-31', '2026-03-01', 0, 'low', 18, 3),
('invoice_records', 'Invoice records', 'finance_database', 'finance', 'financial_record', 'financial_records', '2018-01-01', '2019-12-31', '2026-02-15', 0, 'medium', 42, 5),
('web_logs_2021', 'Web logs 2021', 'log_archive', 'platform_engineering', 'behavioral_log', 'system_logs', '2021-01-01', '2021-12-31', '2022-03-01', 0, 'low', 120, 0),
('environmental_sensor_history', 'Environmental sensor history', 'data_lakehouse', 'research_data_team', 'scientific_observation', 'research_observational_data', '2016-01-01', '2025-12-31', '2026-03-20', 0, 'high', 380, 12),
('terminated_employee_files', 'Terminated employee files', 'hr_document_system', 'human_resources', 'sensitive_personal_data', 'employee_records', '2015-05-01', '2016-05-01', '2026-01-10', 1, 'low', 9, 1),
('model_training_extract_v1', 'Model training extract v1', 'machine_learning_workspace', 'machine_learning', 'derived_personal_data', 'ml_training_extract', '2023-06-01', '2024-06-01', '2024-09-01', 0, 'low', 64, 2),
('legacy_dashboard_extract', 'Legacy dashboard extract', 'business_intelligence', '', 'internal_analytics', 'dashboard_extract', '2020-01-01', '2020-12-31', '2021-06-01', 0, 'low', 27, 0);

CREATE TABLE lifecycle_review AS
SELECT
    a.asset_id,
    a.asset_name,
    a.system_name,
    a.owner,
    a.classification,
    a.retention_category,
    a.legal_hold,
    a.archival_value,
    a.storage_gb,
    a.downstream_dependencies,
    r.retention_years,
    r.default_action,
    r.requires_archival_review,
    date(a.trigger_date, '+' || r.retention_years || ' years') AS retention_expiration_date,
    CASE
        WHEN date('2026-03-31') > date(a.trigger_date, '+' || r.retention_years || ' years')
        THEN 1 ELSE 0
    END AS retention_expired,
    CASE
        WHEN a.legal_hold = 1 THEN 'retain_legal_hold'
        WHEN a.owner IS NULL OR trim(a.owner) = '' THEN 'assign_owner_before_disposition'
        WHEN r.requires_archival_review = 1 AND a.archival_value = 'high' THEN 'archive_review_required'
        WHEN date('2026-03-31') > date(a.trigger_date, '+' || r.retention_years || ' years')
             AND a.downstream_dependencies > 0 THEN 'review_dependencies_before_disposition'
        WHEN date('2026-03-31') > date(a.trigger_date, '+' || r.retention_years || ' years')
             THEN 'eligible_for_disposition'
        WHEN julianday('2026-03-31') - julianday(a.last_accessed_date) > 365
             AND a.archival_value = 'low' THEN 'inactive_monitor_for_future_disposition'
        ELSE 'active_retain'
    END AS lifecycle_status
FROM data_assets a
JOIN retention_rules r
    ON a.retention_category = r.retention_category;

.headers on
.mode column

SELECT * FROM lifecycle_review;

SELECT
    system_name,
    COUNT(*) AS asset_count,
    SUM(storage_gb) AS total_storage_gb,
    SUM(retention_expired) AS expired_assets,
    SUM(CASE WHEN legal_hold = 1 THEN 1 ELSE 0 END) AS legal_holds
FROM lifecycle_review
GROUP BY system_name
ORDER BY total_storage_gb DESC;

SELECT
    asset_id,
    asset_name,
    owner,
    classification,
    lifecycle_status,
    default_action
FROM lifecycle_review
WHERE lifecycle_status <> 'active_retain'
ORDER BY lifecycle_status, asset_id;
