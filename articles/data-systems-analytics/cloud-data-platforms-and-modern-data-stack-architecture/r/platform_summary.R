#!/usr/bin/env Rscript

components <- read.csv("data/stack_components.csv", stringsAsFactors = FALSE)
pipelines <- read.csv("data/pipeline_catalog.csv", stringsAsFactors = FALSE)
costs <- read.csv("data/cost_events.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

layer_summary <- aggregate(
  component_id ~ layer,
  data = components,
  FUN = length
)
names(layer_summary) <- c("layer", "component_count")
write.csv(layer_summary, "outputs/layer_summary_r.csv", row.names = FALSE)

pipeline_summary <- aggregate(
  pipeline_id ~ owner,
  data = pipelines,
  FUN = length
)
names(pipeline_summary) <- c("owner", "pipeline_count")
write.csv(pipeline_summary, "outputs/pipeline_owner_summary_r.csv", row.names = FALSE)

cost_summary <- aggregate(
  estimated_cost ~ service_category,
  data = costs,
  FUN = sum
)
write.csv(cost_summary, "outputs/cost_summary_r.csv", row.names = FALSE)

cat("R platform summary complete\n")
