#!/usr/bin/env Rscript

# R Workflow: Pipeline Runs, Quality Gates, Observability, Lineage, and Readiness Summary

stages <- read.csv("data/pipeline_stages.csv", stringsAsFactors = FALSE)
runs <- read.csv("data/pipeline_runs.csv", stringsAsFactors = FALSE)
gates <- read.csv("data/quality_gates.csv", stringsAsFactors = FALSE)
observability <- read.csv("data/observability_metrics.csv", stringsAsFactors = FALSE)
lineage <- read.csv("data/lineage_edges.csv", stringsAsFactors = FALSE)
backfills <- read.csv("data/backfill_requests.csv", stringsAsFactors = FALSE)
idempotency <- read.csv("data/idempotency_checks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

runs$failure_rate <- runs$failed_rows / runs$input_rows
runs$throughput_rows_per_minute <- runs$output_rows / as.numeric(
  difftime(
    as.POSIXct(runs$finished_at, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
    as.POSIXct(runs$started_at, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC"),
    units = "mins"
  )
)

run_summary <- aggregate(
  cbind(input_rows, output_rows, failed_rows, retry_count, failure_rate, throughput_rows_per_minute) ~ pipeline_name + run_mode + status,
  data = runs,
  FUN = mean
)

gate_summary <- aggregate(
  cbind(threshold, observed_value) ~ pipeline_name + dimension + severity + status,
  data = gates,
  FUN = mean
)
gate_summary$gap_to_threshold <- gate_summary$threshold - gate_summary$observed_value

observability_summary <- aggregate(
  cbind(throughput_rows_per_sec, latency_seconds, lag_seconds, error_rate, watermark_lag_seconds, backpressure_ms) ~ pipeline_name + status,
  data = observability,
  FUN = mean
)

stage_summary <- aggregate(
  stage_id ~ pipeline_name + stage_type + mode + criticality + status,
  data = stages,
  FUN = length
)
names(stage_summary) <- c("pipeline_name", "stage_type", "mode", "criticality", "status", "stage_count")

lineage_summary <- aggregate(
  records_moved ~ pipeline_name + edge_type + lineage_status,
  data = lineage,
  FUN = sum
)

backfill_summary <- aggregate(
  expected_rows ~ pipeline_name + status + owner,
  data = backfills,
  FUN = sum
)

idempotency_summary <- aggregate(
  duplicate_effect_count ~ pipeline_name + stage_name + status,
  data = idempotency,
  FUN = sum
)

write.csv(run_summary, "outputs/pipeline_run_summary_r.csv", row.names = FALSE)
write.csv(gate_summary, "outputs/quality_gate_summary_r.csv", row.names = FALSE)
write.csv(observability_summary, "outputs/observability_summary_r.csv", row.names = FALSE)
write.csv(stage_summary, "outputs/stage_summary_r.csv", row.names = FALSE)
write.csv(lineage_summary, "outputs/lineage_summary_r.csv", row.names = FALSE)
write.csv(backfill_summary, "outputs/backfill_summary_r.csv", row.names = FALSE)
write.csv(idempotency_summary, "outputs/idempotency_summary_r.csv", row.names = FALSE)

cat("R pipeline processing summaries written.\n")
