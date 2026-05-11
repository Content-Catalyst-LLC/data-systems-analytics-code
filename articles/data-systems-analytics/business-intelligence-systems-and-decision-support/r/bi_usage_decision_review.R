#!/usr/bin/env Rscript

# R Workflow: BI Usage, Alert, and Decision Review Summary
#
# This workflow summarizes dashboard certification, alert response,
# and decision-review traceability using base R.

dashboards <- read.csv("data/dashboard_inventory.csv", stringsAsFactors = FALSE)
alerts <- read.csv("data/alert_events.csv", stringsAsFactors = FALSE)
reviews <- read.csv("data/decision_reviews.csv", stringsAsFactors = FALSE)
metrics <- read.csv("data/bi_metrics.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

dashboard_lifecycle <- aggregate(
  dashboard_id ~ domain + certification_status + lifecycle_status,
  data = dashboards,
  FUN = length
)
names(dashboard_lifecycle) <- c("domain", "certification_status", "lifecycle_status", "dashboard_count")

alert_summary <- aggregate(
  time_to_acknowledge_hours ~ dashboard_id,
  data = alerts,
  FUN = mean
)
names(alert_summary) <- c("dashboard_id", "average_acknowledgement_hours")

review_summary <- aggregate(
  action_traceable ~ dashboard_id,
  data = reviews,
  FUN = function(x) mean(tolower(x) == "true")
)
names(review_summary) <- c("dashboard_id", "traceability_rate")

metric_summary <- aggregate(
  quality_score ~ domain + semantic_status,
  data = metrics,
  FUN = mean
)
names(metric_summary) <- c("domain", "semantic_status", "average_quality_score")

write.csv(dashboard_lifecycle, "outputs/dashboard_lifecycle_summary_r.csv", row.names = FALSE)
write.csv(alert_summary, "outputs/alert_response_summary_r.csv", row.names = FALSE)
write.csv(review_summary, "outputs/decision_traceability_summary_r.csv", row.names = FALSE)
write.csv(metric_summary, "outputs/metric_quality_summary_r.csv", row.names = FALSE)

cat("R BI usage, alert, and decision review outputs written.\n")
