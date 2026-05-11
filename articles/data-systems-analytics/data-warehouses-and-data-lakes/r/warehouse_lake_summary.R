#!/usr/bin/env Rscript

# R Workflow: Warehouse, Lake, Lakehouse, Governance, and Workload-Fit Summary

assets <- read.csv("data/data_assets.csv", stringsAsFactors = FALSE)
dims <- read.csv("data/dimensional_model_tables.csv", stringsAsFactors = FALSE)
zones <- read.csv("data/lake_zones.csv", stringsAsFactors = FALSE)
governance <- read.csv("data/governance_controls.csv", stringsAsFactors = FALSE)
costs <- read.csv("data/cost_performance_metrics.csv", stringsAsFactors = FALSE)
lakehouse <- read.csv("data/lakehouse_table_features.csv", stringsAsFactors = FALSE)
workloads <- read.csv("data/workload_requirements.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

asset_summary <- aggregate(
  cbind(row_count, size_gb, freshness_hours, query_frequency_per_day) ~ architecture_zone + storage_form + schema_strategy + governance_status,
  data = assets,
  FUN = function(x) c(asset_count = length(x), mean_value = mean(x), sum_value = sum(x))
)
asset_summary <- do.call(data.frame, asset_summary)

zone_asset_counts <- aggregate(
  asset_id ~ architecture_zone,
  data = assets,
  FUN = length
)
names(zone_asset_counts) <- c("architecture_zone", "asset_count")

governance_summary <- aggregate(
  cbind(metadata_coverage, lineage_coverage, owner_assigned, classification_applied) ~ certification_status + access_policy_status + lifecycle_status,
  data = governance,
  FUN = mean
)

cost_summary <- aggregate(
  cbind(monthly_storage_cost_usd, monthly_compute_cost_usd, mean_query_latency_seconds, p95_query_latency_seconds, scan_efficiency_score) ~ cost_status,
  data = costs,
  FUN = mean
)

dimensional_summary <- aggregate(
  table_id ~ model_role + conformed_dimension + certification_status,
  data = dims,
  FUN = length
)
names(dimensional_summary) <- c("model_role", "conformed_dimension", "certification_status", "table_count")

lakehouse_summary <- aggregate(
  cbind(acid_transactions, schema_evolution, time_travel, partition_evolution, batch_stream_unified, metadata_scalability) ~ open_table_format + table_status,
  data = lakehouse,
  FUN = mean
)

workload_summary <- aggregate(
  workload_id ~ primary_use_case + preferred_architecture + requires_strong_governance + requires_open_format,
  data = workloads,
  FUN = length
)
names(workload_summary) <- c("primary_use_case", "preferred_architecture", "requires_strong_governance", "requires_open_format", "workload_count")

write.csv(asset_summary, "outputs/asset_summary_r.csv", row.names = FALSE)
write.csv(zone_asset_counts, "outputs/zone_asset_counts_r.csv", row.names = FALSE)
write.csv(governance_summary, "outputs/governance_summary_r.csv", row.names = FALSE)
write.csv(cost_summary, "outputs/cost_performance_summary_r.csv", row.names = FALSE)
write.csv(dimensional_summary, "outputs/dimensional_model_summary_r.csv", row.names = FALSE)
write.csv(lakehouse_summary, "outputs/lakehouse_feature_summary_r.csv", row.names = FALSE)
write.csv(workload_summary, "outputs/workload_architecture_summary_r.csv", row.names = FALSE)

cat("R warehouse/lake architecture summaries written.\n")
