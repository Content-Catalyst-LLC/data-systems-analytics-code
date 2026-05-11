#!/usr/bin/env Rscript

# R Workflow: Database Estate, Workloads, Governance, Recovery, and Lineage Summary

systems <- read.csv("data/system_inventory.csv", stringsAsFactors = FALSE)
assets <- read.csv("data/schema_assets.csv", stringsAsFactors = FALSE)
workloads <- read.csv("data/workload_catalog.csv", stringsAsFactors = FALSE)
governance <- read.csv("data/governance_controls.csv", stringsAsFactors = FALSE)
recovery <- read.csv("data/recovery_plans.csv", stringsAsFactors = FALSE)
lineage <- read.csv("data/integration_lineage.csv", stringsAsFactors = FALSE)
risks <- read.csv("data/architecture_risks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

system_summary <- aggregate(
  cbind(records_millions, data_volume_gb) ~ system_type + storage_model + primary_workload + certification_status,
  data = systems,
  FUN = function(x) c(system_count = length(x), total_value = sum(x), mean_value = mean(x))
)
system_summary <- do.call(data.frame, system_summary)

asset_summary <- aggregate(
  cbind(foreign_key_count, constraint_count) ~ asset_type + classification + lineage_status + quality_status + access_status,
  data = assets,
  FUN = mean
)

governance_summary <- aggregate(
  cbind(metadata_coverage, lineage_coverage, owner_assigned, classification_applied) ~ access_policy_status + recovery_test_status + quality_gate_status + certification_status,
  data = governance,
  FUN = mean
)

recovery_summary <- aggregate(
  cbind(recovery_point_objective_minutes, recovery_time_objective_minutes, last_backup_age_minutes, last_restore_test_days_ago) ~ replication_mode + failover_coverage + status,
  data = recovery,
  FUN = mean
)

lineage_summary <- aggregate(
  edge_id ~ flow_type + frequency + lineage_visibility + quality_gate + contract_status + status,
  data = lineage,
  FUN = length
)
names(lineage_summary) <- c("flow_type", "frequency", "lineage_visibility", "quality_gate", "contract_status", "status", "edge_count")

workload_summary <- aggregate(
  cbind(latency_requirement_ms, throughput_requirement_per_minute) ~ workload_type + consistency_need + availability_need + governance_need + status,
  data = workloads,
  FUN = mean
)

risk_summary <- aggregate(
  risk_id ~ risk_area + severity + likelihood + status,
  data = risks,
  FUN = length
)
names(risk_summary) <- c("risk_area", "severity", "likelihood", "status", "risk_count")

write.csv(system_summary, "outputs/system_summary_r.csv", row.names = FALSE)
write.csv(asset_summary, "outputs/asset_summary_r.csv", row.names = FALSE)
write.csv(governance_summary, "outputs/governance_summary_r.csv", row.names = FALSE)
write.csv(recovery_summary, "outputs/recovery_summary_r.csv", row.names = FALSE)
write.csv(lineage_summary, "outputs/lineage_summary_r.csv", row.names = FALSE)
write.csv(workload_summary, "outputs/workload_summary_r.csv", row.names = FALSE)
write.csv(risk_summary, "outputs/architecture_risk_summary_r.csv", row.names = FALSE)

cat("R database architecture summaries written.\n")
