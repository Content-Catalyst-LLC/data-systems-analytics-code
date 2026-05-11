-- 1. System inventory by architecture type.
SELECT system_type, storage_model, primary_workload, certification_status,
       COUNT(*) AS system_count,
       SUM(records_millions) AS total_records_millions,
       SUM(data_volume_gb) AS total_data_volume_gb
FROM system_inventory
GROUP BY system_type, storage_model, primary_workload, certification_status
ORDER BY system_type, storage_model;

-- 2. Assets with partial lineage or quality warnings.
SELECT asset_id, system_id, asset_name, asset_type, grain, lineage_status, quality_status, access_status, lifecycle_status
FROM schema_assets
WHERE lineage_status <> 'complete'
   OR quality_status <> 'pass'
   OR access_status <> 'approved'
   OR lifecycle_status <> 'approved'
ORDER BY system_id, asset_name;

-- 3. Governance controls requiring review.
SELECT s.system_name, g.metadata_coverage, g.lineage_coverage, g.access_policy_status,
       g.recovery_test_status, g.quality_gate_status, g.certification_status
FROM governance_controls g
JOIN system_inventory s ON s.system_id = g.system_id
WHERE g.metadata_coverage < 0.85
   OR g.lineage_coverage < 0.75
   OR g.access_policy_status <> 'approved'
   OR g.recovery_test_status <> 'pass'
   OR g.quality_gate_status <> 'pass'
ORDER BY g.metadata_coverage, g.lineage_coverage;

-- 4. Recovery plans not meeting backup or test targets.
SELECT s.system_name, r.recovery_point_objective_minutes, r.last_backup_age_minutes,
       r.recovery_time_objective_minutes, r.last_restore_test_days_ago,
       r.replication_mode, r.failover_coverage, r.status
FROM recovery_plans r
JOIN system_inventory s ON s.system_id = r.system_id
WHERE r.last_backup_age_minutes > r.recovery_point_objective_minutes
   OR r.last_restore_test_days_ago > 60
   OR r.status <> 'pass'
ORDER BY r.last_restore_test_days_ago DESC;

-- 5. Integration lineage edges requiring review.
SELECT edge_id, source_system, target_system, flow_type, frequency, lineage_visibility,
       transformation_owner, quality_gate, contract_status, status
FROM integration_lineage
WHERE lineage_visibility <> 'complete'
   OR quality_gate <> 'pass'
   OR contract_status <> 'approved'
   OR status <> 'pass'
ORDER BY source_system, target_system;

-- 6. Workloads under architecture review.
SELECT workload_name, workload_type, systems_used, latency_requirement_ms,
       throughput_requirement_per_minute, consistency_need, availability_need, governance_need, status
FROM workload_catalog
WHERE status <> 'good'
ORDER BY governance_need DESC, availability_need DESC;

-- 7. Architecture risks by severity and likelihood.
SELECT risk_area, system_id, severity, likelihood, owner, status, description
FROM architecture_risks
WHERE status <> 'resolved'
ORDER BY severity DESC, likelihood DESC;
