#!/usr/bin/env Rscript

# R Workflow: Data Quality, Incident, Baseline, and Remediation Summary
#
# This workflow summarizes quality checks, observability events, baselines,
# incidents, and lineage impact using base R.

registry <- read.csv("data/dataset_registry.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/quality_checks.csv", stringsAsFactors = FALSE)
events <- read.csv("data/observability_events.csv", stringsAsFactors = FALSE)
baselines <- read.csv("data/baselines.csv", stringsAsFactors = FALSE)
incidents <- read.csv("data/incidents.csv", stringsAsFactors = FALSE)
lineage <- read.csv("data/lineage_impact.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

dimension_summary <- aggregate(
  check_id ~ quality_dimension + status + severity,
  data = checks,
  FUN = length
)
names(dimension_summary) <- c("quality_dimension", "status", "severity", "check_count")

event_summary <- aggregate(
  event_id ~ event_type + alert_status,
  data = events,
  FUN = length
)
names(event_summary) <- c("event_type", "alert_status", "event_count")

baseline_summary <- aggregate(
  baseline_id ~ baseline_type,
  data = baselines,
  FUN = length
)
names(baseline_summary) <- c("baseline_type", "baseline_count")

incident_summary <- aggregate(
  incident_id ~ severity + status + root_cause_category,
  data = incidents,
  FUN = length
)
names(incident_summary) <- c("severity", "status", "root_cause_category", "incident_count")

impact_summary <- aggregate(
  edge_id ~ impact_level + asset_type,
  data = lineage,
  FUN = length
)
names(impact_summary) <- c("impact_level", "asset_type", "dependency_count")

dataset_criticality <- aggregate(
  dataset_id ~ criticality + certification_status,
  data = registry,
  FUN = length
)
names(dataset_criticality) <- c("criticality", "certification_status", "dataset_count")

write.csv(dimension_summary, "outputs/quality_dimension_summary_r.csv", row.names = FALSE)
write.csv(event_summary, "outputs/observability_event_summary_r.csv", row.names = FALSE)
write.csv(baseline_summary, "outputs/baseline_summary_r.csv", row.names = FALSE)
write.csv(incident_summary, "outputs/incident_summary_r.csv", row.names = FALSE)
write.csv(impact_summary, "outputs/lineage_impact_summary_r.csv", row.names = FALSE)
write.csv(dataset_criticality, "outputs/dataset_criticality_summary_r.csv", row.names = FALSE)

cat("R quality and observability summaries written.\n")
