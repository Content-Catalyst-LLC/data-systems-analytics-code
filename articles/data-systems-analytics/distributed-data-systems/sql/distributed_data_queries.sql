-- 1. Cluster node health by region and role.
SELECT region, zone, role, status,
       AVG(cpu_utilization) AS mean_cpu,
       AVG(network_rtt_ms) AS mean_rtt_ms,
       COUNT(*) AS node_count
FROM cluster_nodes
GROUP BY region, zone, role, status
ORDER BY region, zone, role;

-- 2. Shards with lagging or degraded replicas.
SELECT r.shard_id,
       COUNT(*) AS replica_count,
       MAX(r.lag_ops) AS max_lag_ops,
       AVG(r.lag_ops) AS mean_lag_ops,
       SUM(CASE WHEN r.replica_state <> 'in_sync' THEN 1 ELSE 0 END) AS degraded_replicas
FROM replica_status r
GROUP BY r.shard_id
HAVING degraded_replicas > 0 OR max_lag_ops > 50
ORDER BY max_lag_ops DESC;

-- 3. Quorum policies and read-write intersection.
SELECT policy_id, workload, replication_factor, read_quorum, write_quorum,
       CASE WHEN read_quorum + write_quorum > replication_factor THEN 1 ELSE 0 END AS read_write_intersect,
       consistency_model, availability_orientation, status
FROM quorum_policies
ORDER BY workload;

-- 4. Operations with consistency or quorum warnings.
SELECT operation_id, shard_id, operation_type, client_region, latency_ms, result_status, consistency_observed
FROM operation_log
WHERE result_status <> 'committed'
   OR consistency_observed IN ('stale_possible', 'quorum_not_met')
ORDER BY latency_ms DESC;

-- 5. Conflicts requiring stewardship.
SELECT conflict_id, shard_id, key_id, resolution_strategy, resolution_status, owner
FROM conflict_records
WHERE resolution_status <> 'resolved'
ORDER BY detected_at;

-- 6. Consensus events requiring attention.
SELECT event_id, shard_id, event_type, term, leader_node, result, notes
FROM consensus_events
WHERE result <> 'success'
ORDER BY event_time;

-- 7. Failover drills with warning status.
SELECT drill_id, scenario, affected_shard, primary_node, replacement_node, recovery_time_seconds, data_loss_observed, drill_status
FROM failover_drills
WHERE drill_status <> 'pass'
ORDER BY recovery_time_seconds DESC;
