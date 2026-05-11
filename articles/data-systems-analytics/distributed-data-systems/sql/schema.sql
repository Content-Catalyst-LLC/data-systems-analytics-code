CREATE TABLE IF NOT EXISTS cluster_nodes (
    node_id TEXT PRIMARY KEY,
    region TEXT NOT NULL,
    zone TEXT NOT NULL,
    role TEXT NOT NULL,
    status TEXT NOT NULL,
    storage_gb REAL NOT NULL,
    cpu_utilization REAL NOT NULL,
    network_rtt_ms REAL NOT NULL,
    last_heartbeat TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shard_map (
    shard_id TEXT PRIMARY KEY,
    key_range_start INTEGER NOT NULL,
    key_range_end INTEGER NOT NULL,
    leader_node TEXT NOT NULL,
    replica_nodes TEXT NOT NULL,
    replication_factor INTEGER NOT NULL,
    partition_strategy TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS replica_status (
    replica_id TEXT PRIMARY KEY,
    shard_id TEXT NOT NULL,
    node_id TEXT NOT NULL,
    is_leader INTEGER NOT NULL,
    commit_index INTEGER NOT NULL,
    applied_index INTEGER NOT NULL,
    lag_ops INTEGER NOT NULL,
    replica_state TEXT NOT NULL,
    last_snapshot_time TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS quorum_policies (
    policy_id TEXT PRIMARY KEY,
    workload TEXT NOT NULL,
    replication_factor INTEGER NOT NULL,
    read_quorum INTEGER NOT NULL,
    write_quorum INTEGER NOT NULL,
    consistency_model TEXT NOT NULL,
    availability_orientation TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS operation_log (
    operation_id TEXT PRIMARY KEY,
    shard_id TEXT NOT NULL,
    operation_type TEXT NOT NULL,
    client_region TEXT NOT NULL,
    request_time TEXT NOT NULL,
    commit_time TEXT NOT NULL,
    read_quorum_observed INTEGER NOT NULL,
    write_quorum_observed INTEGER NOT NULL,
    latency_ms REAL NOT NULL,
    result_status TEXT NOT NULL,
    consistency_observed TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS conflict_records (
    conflict_id TEXT PRIMARY KEY,
    shard_id TEXT NOT NULL,
    key_id TEXT NOT NULL,
    replica_versions TEXT NOT NULL,
    detected_at TEXT NOT NULL,
    resolution_strategy TEXT NOT NULL,
    resolution_status TEXT NOT NULL,
    owner TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS consensus_events (
    event_id TEXT PRIMARY KEY,
    shard_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    term INTEGER NOT NULL,
    leader_node TEXT NOT NULL,
    event_time TEXT NOT NULL,
    result TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS failover_drills (
    drill_id TEXT PRIMARY KEY,
    scenario TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT NOT NULL,
    affected_shard TEXT NOT NULL,
    primary_node TEXT NOT NULL,
    replacement_node TEXT NOT NULL,
    recovery_time_seconds REAL NOT NULL,
    data_loss_observed INTEGER NOT NULL,
    drill_status TEXT NOT NULL
);
