#!/usr/bin/env Rscript

# R Workflow: Event-Time Lateness, Window Summaries, Watermark Lag, and Streaming Governance

events <- read.csv("data/event_stream.csv", stringsAsFactors = FALSE)
topics <- read.csv("data/stream_topic_registry.csv", stringsAsFactors = FALSE)
windows <- read.csv("data/window_definitions.csv", stringsAsFactors = FALSE)
watermarks <- read.csv("data/watermark_observations.csv", stringsAsFactors = FALSE)
governance <- read.csv("data/governance_checks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

events$event_time_posix <- as.POSIXct(events$event_time, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
events$processing_time_posix <- as.POSIXct(events$processing_time, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
events$lateness_seconds <- as.numeric(difftime(events$processing_time_posix, events$event_time_posix, units = "secs"))

events$window_start <- as.POSIXct(floor(as.numeric(events$event_time_posix) / 60) * 60, origin = "1970-01-01", tz = "UTC")

window_summary <- aggregate(
  cbind(value, quantity) ~ window_start + event_type,
  data = events,
  FUN = function(x) c(n = length(x), mean = mean(x), sum = sum(x))
)
window_summary <- do.call(data.frame, window_summary)

lateness_summary <- aggregate(
  lateness_seconds ~ event_type + source_system,
  data = events,
  FUN = function(x) c(n = length(x), mean = mean(x), p95 = quantile(x, 0.95), max = max(x))
)
lateness_summary <- do.call(data.frame, lateness_summary)

watermarks$processing_time_posix <- as.POSIXct(watermarks$processing_time, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
watermarks$watermark_time_posix <- as.POSIXct(watermarks$watermark_time, format = "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")
watermarks$watermark_lag_seconds <- as.numeric(difftime(watermarks$processing_time_posix, watermarks$watermark_time_posix, units = "secs"))

watermark_summary <- aggregate(
  cbind(late_event_count, state_size_mb, backpressure_ms, watermark_lag_seconds) ~ stream_name + status,
  data = watermarks,
  FUN = mean
)

topic_summary <- aggregate(
  topic_id ~ event_domain + delivery_semantics + status + risk_level,
  data = topics,
  FUN = length
)
names(topic_summary) <- c("event_domain", "delivery_semantics", "status", "risk_level", "topic_count")

governance_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = governance,
  FUN = length
)
names(governance_summary) <- c("check_type", "status", "severity", "check_count")

window_policy_summary <- aggregate(
  window_id ~ window_type + trigger_policy + output_mode + status,
  data = windows,
  FUN = length
)
names(window_policy_summary) <- c("window_type", "trigger_policy", "output_mode", "status", "window_count")

write.csv(window_summary, "outputs/window_summary_r.csv", row.names = FALSE)
write.csv(lateness_summary, "outputs/lateness_summary_r.csv", row.names = FALSE)
write.csv(watermark_summary, "outputs/watermark_summary_r.csv", row.names = FALSE)
write.csv(topic_summary, "outputs/topic_summary_r.csv", row.names = FALSE)
write.csv(governance_summary, "outputs/governance_summary_r.csv", row.names = FALSE)
write.csv(window_policy_summary, "outputs/window_policy_summary_r.csv", row.names = FALSE)

cat("R streaming analytics summaries written.\n")
