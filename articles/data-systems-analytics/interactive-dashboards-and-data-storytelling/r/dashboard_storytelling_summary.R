#!/usr/bin/env Rscript

# R Workflow: Dashboard, KPI, Filter, Story, Annotation, Accessibility, and Governance Summary

dashboards <- read.csv("data/dashboard_inventory.csv", stringsAsFactors = FALSE)
kpis <- read.csv("data/kpi_definitions.csv", stringsAsFactors = FALSE)
filters <- read.csv("data/filter_controls.csv", stringsAsFactors = FALSE)
views <- read.csv("data/linked_views.csv", stringsAsFactors = FALSE)
stories <- read.csv("data/story_points.csv", stringsAsFactors = FALSE)
annotations <- read.csv("data/annotations.csv", stringsAsFactors = FALSE)
interactions <- read.csv("data/interaction_events.csv", stringsAsFactors = FALSE)
accessibility <- read.csv("data/accessibility_checks.csv", stringsAsFactors = FALSE)
governance <- read.csv("data/governance_checks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

dashboard_summary <- aggregate(
  dashboard_id ~ dashboard_type + status + refresh_cadence,
  data = dashboards,
  FUN = length
)
names(dashboard_summary) <- c("dashboard_type", "status", "refresh_cadence", "dashboard_count")

kpi_summary <- aggregate(
  kpi_id ~ definition_status + certification_status,
  data = kpis,
  FUN = length
)
names(kpi_summary) <- c("definition_status", "certification_status", "kpi_count")

filter_summary <- aggregate(
  filter_id ~ filter_type + complexity_level + default_state_visible + reset_available,
  data = filters,
  FUN = length
)
names(filter_summary) <- c("filter_type", "complexity_level", "default_state_visible", "reset_available", "filter_count")

view_summary <- aggregate(
  view_id ~ visual_type + purpose + design_risk + caption_quality,
  data = views,
  FUN = length
)
names(view_summary) <- c("visual_type", "purpose", "design_risk", "caption_quality", "view_count")

story_summary <- aggregate(
  story_point_id ~ story_function + uncertainty_visible,
  data = stories,
  FUN = length
)
names(story_summary) <- c("story_function", "uncertainty_visible", "story_point_count")

annotation_summary <- aggregate(
  annotation_id ~ annotation_type + text_quality + emphasis_risk,
  data = annotations,
  FUN = length
)
names(annotation_summary) <- c("annotation_type", "text_quality", "emphasis_risk", "annotation_count")

interaction_summary <- aggregate(
  event_id ~ event_type + friction_level + error_risk,
  data = interactions,
  FUN = length
)
names(interaction_summary) <- c("event_type", "friction_level", "error_risk", "interaction_count")

accessibility_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = accessibility,
  FUN = length
)
names(accessibility_summary) <- c("check_type", "status", "severity", "check_count")

governance_summary <- aggregate(
  governance_id ~ check_type + status + blocking_issue,
  data = governance,
  FUN = length
)
names(governance_summary) <- c("check_type", "status", "blocking_issue", "governance_check_count")

write.csv(dashboard_summary, "outputs/dashboard_summary_r.csv", row.names = FALSE)
write.csv(kpi_summary, "outputs/kpi_summary_r.csv", row.names = FALSE)
write.csv(filter_summary, "outputs/filter_summary_r.csv", row.names = FALSE)
write.csv(view_summary, "outputs/view_summary_r.csv", row.names = FALSE)
write.csv(story_summary, "outputs/story_summary_r.csv", row.names = FALSE)
write.csv(annotation_summary, "outputs/annotation_summary_r.csv", row.names = FALSE)
write.csv(interaction_summary, "outputs/interaction_summary_r.csv", row.names = FALSE)
write.csv(accessibility_summary, "outputs/accessibility_summary_r.csv", row.names = FALSE)
write.csv(governance_summary, "outputs/governance_summary_r.csv", row.names = FALSE)

cat("R dashboard and storytelling summaries written.\n")
