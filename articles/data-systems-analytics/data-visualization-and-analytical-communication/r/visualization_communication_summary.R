#!/usr/bin/env Rscript

# R Workflow: Chart, Encoding, Uncertainty, Annotation, Accessibility, and Review Summary

visuals <- read.csv("data/visualization_inventory.csv", stringsAsFactors = FALSE)
charts <- read.csv("data/chart_assessments.csv", stringsAsFactors = FALSE)
encodings <- read.csv("data/encoding_assessments.csv", stringsAsFactors = FALSE)
uncertainty <- read.csv("data/uncertainty_elements.csv", stringsAsFactors = FALSE)
annotations <- read.csv("data/annotation_elements.csv", stringsAsFactors = FALSE)
accessibility <- read.csv("data/accessibility_checks.csv", stringsAsFactors = FALSE)
evidence <- read.csv("data/evidence_links.csv", stringsAsFactors = FALSE)
reviews <- read.csv("data/review_checkpoints.csv", stringsAsFactors = FALSE)
outputs <- read.csv("data/visual_outputs.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

visual_summary <- aggregate(
  visual_id ~ visualization_context + status + publication_surface,
  data = visuals,
  FUN = length
)
names(visual_summary) <- c("visualization_context", "status", "publication_surface", "visual_count")

chart_summary <- aggregate(
  chart_id ~ chart_type + analytical_task + chart_fit,
  data = charts,
  FUN = length
)
names(chart_summary) <- c("chart_type", "analytical_task", "chart_fit", "chart_count")

encoding_summary <- aggregate(
  encoding_id ~ primary_encoding + perceptual_accuracy + color_dependency,
  data = encodings,
  FUN = length
)
names(encoding_summary) <- c("primary_encoding", "perceptual_accuracy", "color_dependency", "encoding_count")

uncertainty_summary <- aggregate(
  uncertainty_id ~ uncertainty_type + visual_form + near_claim + statement_quality,
  data = uncertainty,
  FUN = length
)
names(uncertainty_summary) <- c("uncertainty_type", "visual_form", "near_claim", "statement_quality", "uncertainty_count")

annotation_summary <- aggregate(
  annotation_id ~ annotation_type + text_quality + emphasis_risk,
  data = annotations,
  FUN = length
)
names(annotation_summary) <- c("annotation_type", "text_quality", "emphasis_risk", "annotation_count")

accessibility_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = accessibility,
  FUN = length
)
names(accessibility_summary) <- c("check_type", "status", "severity", "check_count")

traceability_summary <- aggregate(
  link_id ~ traceability_status + review_status,
  data = evidence,
  FUN = length
)
names(traceability_summary) <- c("traceability_status", "review_status", "link_count")

review_summary <- aggregate(
  review_id ~ review_type + status,
  data = reviews,
  FUN = length
)
names(review_summary) <- c("review_type", "status", "review_count")

output_summary <- aggregate(
  output_id ~ output_format + versioned + archived + hash_recorded,
  data = outputs,
  FUN = length
)
names(output_summary) <- c("output_format", "versioned", "archived", "hash_recorded", "output_count")

write.csv(visual_summary, "outputs/visual_summary_r.csv", row.names = FALSE)
write.csv(chart_summary, "outputs/chart_summary_r.csv", row.names = FALSE)
write.csv(encoding_summary, "outputs/encoding_summary_r.csv", row.names = FALSE)
write.csv(uncertainty_summary, "outputs/uncertainty_summary_r.csv", row.names = FALSE)
write.csv(annotation_summary, "outputs/annotation_summary_r.csv", row.names = FALSE)
write.csv(accessibility_summary, "outputs/accessibility_summary_r.csv", row.names = FALSE)
write.csv(traceability_summary, "outputs/traceability_summary_r.csv", row.names = FALSE)
write.csv(review_summary, "outputs/review_summary_r.csv", row.names = FALSE)
write.csv(output_summary, "outputs/output_summary_r.csv", row.names = FALSE)

cat("R visualization and analytical communication summaries written.\n")
