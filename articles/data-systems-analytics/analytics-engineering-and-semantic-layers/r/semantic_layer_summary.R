#!/usr/bin/env Rscript

# R Workflow: Semantic Metric, Model, and Consumption Summary
#
# This workflow summarizes analytics models, semantic metrics, test status,
# definition drift, and metric consumption using base R.

models <- read.csv("data/model_registry.csv", stringsAsFactors = FALSE)
metrics <- read.csv("data/semantic_metrics.csv", stringsAsFactors = FALSE)
tests <- read.csv("data/model_tests.csv", stringsAsFactors = FALSE)
usage <- read.csv("data/metric_usage.csv", stringsAsFactors = FALSE)
drift <- read.csv("data/definition_drift.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

model_layer_summary <- aggregate(
  model_id ~ layer + lifecycle_status,
  data = models,
  FUN = length
)
names(model_layer_summary) <- c("layer", "lifecycle_status", "model_count")

metric_certification_summary <- aggregate(
  metric_id ~ domain + certification_status,
  data = metrics,
  FUN = length
)
names(metric_certification_summary) <- c("domain", "certification_status", "metric_count")

test_summary <- aggregate(
  test_id ~ status + test_type,
  data = tests,
  FUN = length
)
names(test_summary) <- c("status", "test_type", "test_count")

usage_summary <- aggregate(
  cbind(query_count, dashboard_views, notebook_sessions) ~ metric_id,
  data = usage,
  FUN = sum
)

drift_summary <- aggregate(
  local_definition_count ~ drift_status,
  data = drift,
  FUN = mean
)
names(drift_summary) <- c("drift_status", "average_local_definition_count")

write.csv(model_layer_summary, "outputs/model_layer_summary_r.csv", row.names = FALSE)
write.csv(metric_certification_summary, "outputs/metric_certification_summary_r.csv", row.names = FALSE)
write.csv(test_summary, "outputs/model_test_summary_r.csv", row.names = FALSE)
write.csv(usage_summary, "outputs/metric_usage_summary_r.csv", row.names = FALSE)
write.csv(drift_summary, "outputs/definition_drift_summary_r.csv", row.names = FALSE)

cat("R semantic layer summary outputs written.\n")
