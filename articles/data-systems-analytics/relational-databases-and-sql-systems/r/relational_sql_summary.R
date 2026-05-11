#!/usr/bin/env Rscript

# R Workflow: Relational Schema, Constraints, Workloads, Transactions, and Governance Summary

schema <- read.csv("data/relational_schema_inventory.csv", stringsAsFactors = FALSE)
constraints <- read.csv("data/constraint_inventory.csv", stringsAsFactors = FALSE)
workloads <- read.csv("data/query_workload.csv", stringsAsFactors = FALSE)
indexes <- read.csv("data/index_inventory.csv", stringsAsFactors = FALSE)
normalization <- read.csv("data/normalization_checks.csv", stringsAsFactors = FALSE)
transactions <- read.csv("data/transaction_log_sample.csv", stringsAsFactors = FALSE)
access <- read.csv("data/access_controls.csv", stringsAsFactors = FALSE)
incidents <- read.csv("data/integrity_incidents.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

schema_summary <- aggregate(
  row_count ~ entity_type + normalization_target + certification_status,
  data = schema,
  FUN = function(x) c(table_count = length(x), total_rows = sum(x), mean_rows = mean(x))
)
schema_summary <- do.call(data.frame, schema_summary)

constraint_summary <- aggregate(
  constraint_id ~ table_name + constraint_type + severity + status,
  data = constraints,
  FUN = length
)
names(constraint_summary) <- c("table_name", "constraint_type", "severity", "status", "constraint_count")

workloads$p95_to_expected_ratio <- workloads$p95_latency_ms / workloads$expected_latency_ms
workload_summary <- aggregate(
  cbind(expected_latency_ms, p95_latency_ms, p95_to_expected_ratio, execution_count_per_day) ~ query_type + criticality + status,
  data = workloads,
  FUN = mean
)

index_summary <- aggregate(
  write_overhead_score ~ table_name + index_type + unique_index + covering_index + status,
  data = indexes,
  FUN = function(x) c(index_count = length(x), mean_write_overhead = mean(x))
)
index_summary <- do.call(data.frame, index_summary)

normalization_summary <- aggregate(
  check_id ~ normal_form + duplication_risk + update_anomaly_risk + status,
  data = normalization,
  FUN = length
)
names(normalization_summary) <- c("normal_form", "duplication_risk", "update_anomaly_risk", "status", "check_count")

transaction_summary <- aggregate(
  cbind(operation_count, rollback_flag, deadlock_retry_count, latency_ms) ~ isolation_level + result,
  data = transactions,
  FUN = mean
)

access_summary <- aggregate(
  grant_id ~ role_name + privilege + least_privilege_status + row_level_security + masking_required + status,
  data = access,
  FUN = length
)
names(access_summary) <- c("role_name", "privilege", "least_privilege_status", "row_level_security", "masking_required", "status", "grant_count")

incident_summary <- aggregate(
  affected_rows ~ table_name + incident_type + severity + status,
  data = incidents,
  FUN = sum
)

write.csv(schema_summary, "outputs/schema_summary_r.csv", row.names = FALSE)
write.csv(constraint_summary, "outputs/constraint_summary_r.csv", row.names = FALSE)
write.csv(workload_summary, "outputs/query_workload_summary_r.csv", row.names = FALSE)
write.csv(index_summary, "outputs/index_summary_r.csv", row.names = FALSE)
write.csv(normalization_summary, "outputs/normalization_summary_r.csv", row.names = FALSE)
write.csv(transaction_summary, "outputs/transaction_summary_r.csv", row.names = FALSE)
write.csv(access_summary, "outputs/access_control_summary_r.csv", row.names = FALSE)
write.csv(incident_summary, "outputs/integrity_incident_summary_r.csv", row.names = FALSE)

cat("R relational SQL summaries written.\n")
