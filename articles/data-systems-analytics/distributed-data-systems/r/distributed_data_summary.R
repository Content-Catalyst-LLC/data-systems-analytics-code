#!/usr/bin/env Rscript

# R Workflow: Distributed Cluster, Replica Lag, Quorum Policy, Conflict, and Failover Summary

nodes <- read.csv("data/cluster_nodes.csv", stringsAsFactors = FALSE)
shards <- read.csv("data/shard_map.csv", stringsAsFactors = FALSE)
replicas <- read.csv("data/replica_status.csv", stringsAsFactors = FALSE)
policies <- read.csv("data/quorum_policies.csv", stringsAsFactors = FALSE)
operations <- read.csv("data/operation_log.csv", stringsAsFactors = FALSE)
conflicts <- read.csv("data/conflict_records.csv", stringsAsFactors = FALSE)
consensus <- read.csv("data/consensus_events.csv", stringsAsFactors = FALSE)
failovers <- read.csv("data/failover_drills.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

node_summary <- aggregate(
  cbind(storage_gb, cpu_utilization, network_rtt_ms) ~ region + role + status,
  data = nodes,
  FUN = mean
)

replica_lag_summary <- aggregate(
  lag_ops ~ shard_id + replica_state,
  data = replicas,
  FUN = function(x) c(replica_count = length(x), mean_lag = mean(x), max_lag = max(x))
)
replica_lag_summary <- do.call(data.frame, replica_lag_summary)
names(replica_lag_summary) <- c("shard_id", "replica_state", "replica_count", "mean_lag_ops", "max_lag_ops")

policies$quorum_intersection <- ifelse(
  policies$read_quorum + policies$write_quorum > policies$replication_factor,
  1,
  0
)

quorum_summary <- aggregate(
  quorum_intersection ~ availability_orientation + consistency_model + status,
  data = policies,
  FUN = mean
)

operations$latency_ms <- as.numeric(operations$latency_ms)
operation_summary <- aggregate(
  latency_ms ~ shard_id + operation_type + result_status + consistency_observed,
  data = operations,
  FUN = function(x) c(operation_count = length(x), mean_latency = mean(x), max_latency = max(x))
)
operation_summary <- do.call(data.frame, operation_summary)
names(operation_summary) <- c(
  "shard_id",
  "operation_type",
  "result_status",
  "consistency_observed",
  "operation_count",
  "mean_latency_ms",
  "max_latency_ms"
)

conflict_summary <- aggregate(
  conflict_id ~ shard_id + resolution_strategy + resolution_status,
  data = conflicts,
  FUN = length
)
names(conflict_summary) <- c("shard_id", "resolution_strategy", "resolution_status", "conflict_count")

consensus_summary <- aggregate(
  event_id ~ shard_id + event_type + result,
  data = consensus,
  FUN = length
)
names(consensus_summary) <- c("shard_id", "event_type", "result", "event_count")

failover_summary <- aggregate(
  recovery_time_seconds ~ scenario + drill_status,
  data = failovers,
  FUN = function(x) c(drill_count = length(x), mean_recovery_time = mean(x), max_recovery_time = max(x))
)
failover_summary <- do.call(data.frame, failover_summary)
names(failover_summary) <- c("scenario", "drill_status", "drill_count", "mean_recovery_time_seconds", "max_recovery_time_seconds")

write.csv(node_summary, "outputs/node_summary_r.csv", row.names = FALSE)
write.csv(replica_lag_summary, "outputs/replica_lag_summary_r.csv", row.names = FALSE)
write.csv(quorum_summary, "outputs/quorum_summary_r.csv", row.names = FALSE)
write.csv(operation_summary, "outputs/operation_summary_r.csv", row.names = FALSE)
write.csv(conflict_summary, "outputs/conflict_summary_r.csv", row.names = FALSE)
write.csv(consensus_summary, "outputs/consensus_summary_r.csv", row.names = FALSE)
write.csv(failover_summary, "outputs/failover_summary_r.csv", row.names = FALSE)

cat("R distributed data summaries written.\n")
