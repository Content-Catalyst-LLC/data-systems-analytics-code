#!/usr/bin/env Rscript

# R Workflow: Feature Registry, Encoding, Leakage, Selection, and Representation Summary

registry <- read.csv("data/feature_registry.csv", stringsAsFactors = FALSE)
rules <- read.csv("data/transformation_rules.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/feature_quality_checks.csv", stringsAsFactors = FALSE)
selection <- read.csv("data/selection_scores.csv", stringsAsFactors = FALSE)
representations <- read.csv("data/representation_metrics.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

family_summary <- aggregate(
  feature_id ~ feature_family + status + leakage_risk,
  data = registry,
  FUN = length
)
names(family_summary) <- c("feature_family", "status", "leakage_risk", "feature_count")

rule_summary <- aggregate(
  rule_id ~ rule_type + fit_scope + allowed_at_prediction_time + review_status,
  data = rules,
  FUN = length
)
names(rule_summary) <- c("rule_type", "fit_scope", "allowed_at_prediction_time", "review_status", "rule_count")

quality_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = checks,
  FUN = length
)
names(quality_summary) <- c("check_type", "status", "severity", "check_count")

selection_summary <- aggregate(
  selection_id ~ selection_method + selected + selection_status,
  data = selection,
  FUN = length
)
names(selection_summary) <- c("selection_method", "selected", "selection_status", "feature_count")

representation_summary <- aggregate(
  cbind(feature_count, sparsity_ratio, oov_rate, leakage_flag_count, approved_feature_share) ~ status,
  data = representations,
  FUN = mean
)

write.csv(family_summary, "outputs/feature_family_summary_r.csv", row.names = FALSE)
write.csv(rule_summary, "outputs/transformation_rule_summary_r.csv", row.names = FALSE)
write.csv(quality_summary, "outputs/feature_quality_summary_r.csv", row.names = FALSE)
write.csv(selection_summary, "outputs/feature_selection_summary_r.csv", row.names = FALSE)
write.csv(representation_summary, "outputs/representation_summary_r.csv", row.names = FALSE)

cat("R feature engineering summaries written.\n")
