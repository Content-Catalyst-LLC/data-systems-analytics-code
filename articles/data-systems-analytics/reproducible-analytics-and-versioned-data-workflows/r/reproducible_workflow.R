#!/usr/bin/env Rscript

input_path <- "data/sample_events.csv"
output_path <- "outputs/run_summary_r.csv"
manifest_path <- "outputs/run_manifest_r.txt"

events <- read.csv(input_path, stringsAsFactors = FALSE)
summary <- aggregate(value ~ system, data = events, FUN = function(x) c(records = length(x), total = sum(x), average = mean(x)))

summary_flat <- data.frame(
  system = summary$system,
  records = summary$value[, "records"],
  total_value = summary$value[, "total"],
  average_value = round(summary$value[, "average"], 2)
)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)
write.csv(summary_flat, output_path, row.names = FALSE)

manifest <- c(
  paste("workflow=reproducible-analytics-and-versioned-data-workflows"),
  paste("runtime=R"),
  paste("r_version=", R.version.string, sep = ""),
  paste("input_path=", input_path, sep = ""),
  paste("output_path=", output_path, sep = ""),
  paste("row_count=", nrow(events), sep = ""),
  paste("run_time_utc=", format(Sys.time(), tz = "UTC", usetz = TRUE), sep = "")
)

writeLines(manifest, manifest_path)
cat("R workflow complete\n")
