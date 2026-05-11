#!/usr/bin/env Rscript

# R Workflow: Causal Study Registry, Design, Estimand, and Assumption Summary

registry <- read.csv("data/causal_study_registry.csv", stringsAsFactors = FALSE)
units <- read.csv("data/experiment_units.csv", stringsAsFactors = FALSE)
did <- read.csv("data/did_panel.csv", stringsAsFactors = FALSE)
rdd <- read.csv("data/rdd_units.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/assumption_checks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

design_summary <- aggregate(
  study_id ~ design_type + estimand + status + risk_level,
  data = registry,
  FUN = length
)
names(design_summary) <- c("design_type", "estimand", "status", "risk_level", "study_count")

ate_summary <- aggregate(
  outcome ~ study_id + treatment,
  data = units,
  FUN = mean
)
names(ate_summary) <- c("study_id", "treatment", "mean_outcome")

did_summary <- aggregate(
  outcome ~ group + post,
  data = did,
  FUN = mean
)

treated_change <- with(did_summary, outcome[group == "treated" & post == 1] - outcome[group == "treated" & post == 0])
control_change <- with(did_summary, outcome[group == "control" & post == 1] - outcome[group == "control" & post == 0])
did_estimate <- data.frame(
  study_id = "study003",
  treated_change = treated_change,
  control_change = control_change,
  difference_in_differences = treated_change - control_change
)

rdd_near <- rdd[abs(rdd$running_variable - rdd$cutoff) <= 2, ]
rdd_summary <- aggregate(
  outcome ~ study_id + treatment,
  data = rdd_near,
  FUN = mean
)

assumption_summary <- aggregate(
  check_id ~ assumption + status + severity,
  data = checks,
  FUN = length
)
names(assumption_summary) <- c("assumption", "status", "severity", "check_count")

write.csv(design_summary, "outputs/design_summary_r.csv", row.names = FALSE)
write.csv(ate_summary, "outputs/ate_summary_r.csv", row.names = FALSE)
write.csv(did_estimate, "outputs/did_estimate_r.csv", row.names = FALSE)
write.csv(rdd_summary, "outputs/rdd_summary_r.csv", row.names = FALSE)
write.csv(assumption_summary, "outputs/assumption_summary_r.csv", row.names = FALSE)

cat("R causal inference summaries written.\n")
