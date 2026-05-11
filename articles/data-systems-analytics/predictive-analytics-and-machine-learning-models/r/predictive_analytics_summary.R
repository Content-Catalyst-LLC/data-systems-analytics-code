#!/usr/bin/env Rscript

# R Workflow: Predictive Model Registry, Metrics, Thresholds, and Monitoring Summary

models <- read.csv("data/model_registry.csv", stringsAsFactors = FALSE)
splits <- read.csv("data/training_validation_splits.csv", stringsAsFactors = FALSE)
metrics <- read.csv("data/metric_scorecard.csv", stringsAsFactors = FALSE)
thresholds <- read.csv("data/threshold_policies.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/leakage_shift_checks.csv", stringsAsFactors = FALSE)
monitoring <- read.csv("data/monitoring_windows.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

model_summary <- aggregate(
  model_id ~ task_type + model_family + status + risk_level,
  data = models,
  FUN = length
)
names(model_summary) <- c("task_type", "model_family", "status", "risk_level", "model_count")

split_summary <- aggregate(
  split_id ~ split_strategy + stratified + time_ordered + group_aware + test_set_protected + status,
  data = splits,
  FUN = length
)
names(split_summary) <- c(
  "split_strategy", "stratified", "time_ordered", "group_aware",
  "test_set_protected", "status", "split_count"
)

metric_summary <- aggregate(
  metric_id ~ metric_family + metric_name + status,
  data = metrics,
  FUN = length
)
names(metric_summary) <- c("metric_family", "metric_name", "status", "metric_count")

threshold_summary <- aggregate(
  policy_id ~ model_id + review_status,
  data = thresholds,
  FUN = length
)
names(threshold_summary) <- c("model_id", "review_status", "threshold_policy_count")

check_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = checks,
  FUN = length
)
names(check_summary) <- c("check_type", "status", "severity", "check_count")

monitoring_summary <- aggregate(
  drift_index ~ model_id + production_metric + status,
  data = monitoring,
  FUN = mean
)
names(monitoring_summary) <- c("model_id", "production_metric", "status", "mean_drift_index")

write.csv(model_summary, "outputs/model_summary_r.csv", row.names = FALSE)
write.csv(split_summary, "outputs/split_summary_r.csv", row.names = FALSE)
write.csv(metric_summary, "outputs/metric_summary_r.csv", row.names = FALSE)
write.csv(threshold_summary, "outputs/threshold_summary_r.csv", row.names = FALSE)
write.csv(check_summary, "outputs/leakage_shift_check_summary_r.csv", row.names = FALSE)
write.csv(monitoring_summary, "outputs/monitoring_summary_r.csv", row.names = FALSE)

cat("R predictive analytics summaries written.\n")
