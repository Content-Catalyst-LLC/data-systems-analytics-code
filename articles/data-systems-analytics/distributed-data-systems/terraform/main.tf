terraform {
  required_version = ">= 1.6.0"
}

locals {
  distributed_data_capabilities = [
    "partitioning",
    "replication",
    "quorum_reads_and_writes",
    "leader_election",
    "consensus_metadata",
    "replica_lag_monitoring",
    "conflict_resolution",
    "failover_drills",
    "repair_and_rebalancing",
    "distributed_observability"
  ]
}

output "distributed_data_capabilities" {
  value = local.distributed_data_capabilities
}
