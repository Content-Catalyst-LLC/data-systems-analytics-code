#!/usr/bin/env Rscript

# R Workflow: Estimation, Confidence Intervals, Regression, Diagnostics, and Readiness Summary

observations <- read.csv("data/sample_observations.csv", stringsAsFactors = FALSE)
registry <- read.csv("data/model_registry.csv", stringsAsFactors = FALSE)
claims <- read.csv("data/inference_claims.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/diagnostic_checks.csv", stringsAsFactors = FALSE)
robustness <- read.csv("data/robustness_checks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

group_summary <- aggregate(
  outcome ~ group_id,
  data = observations,
  FUN = function(x) c(n = length(x), mean = mean(x), sd = sd(x), se = sd(x) / sqrt(length(x)))
)
group_summary <- do.call(data.frame, group_summary)
names(group_summary) <- c("group_id", "n", "mean", "sd", "standard_error")
group_summary$ci_low <- group_summary$mean - 1.96 * group_summary$standard_error
group_summary$ci_high <- group_summary$mean + 1.96 * group_summary$standard_error

fit <- lm(outcome ~ predictor_x + predictor_z, data = observations)
regression_summary <- data.frame(
  term = rownames(summary(fit)$coefficients),
  estimate = summary(fit)$coefficients[, 1],
  standard_error = summary(fit)$coefficients[, 2],
  t_value = summary(fit)$coefficients[, 3],
  p_value = summary(fit)$coefficients[, 4],
  row.names = NULL
)

diagnostic_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = checks,
  FUN = length
)
names(diagnostic_summary) <- c("check_type", "status", "severity", "check_count")

claim_summary <- aggregate(
  claim_id ~ claim_type + claim_status,
  data = claims,
  FUN = length
)
names(claim_summary) <- c("claim_type", "claim_status", "claim_count")

robustness_summary <- aggregate(
  robustness_id ~ check_name + status,
  data = robustness,
  FUN = length
)
names(robustness_summary) <- c("check_name", "status", "robustness_check_count")

model_summary <- aggregate(
  model_id ~ model_family + estimand + status + risk_level,
  data = registry,
  FUN = length
)
names(model_summary) <- c("model_family", "estimand", "status", "risk_level", "model_count")

write.csv(group_summary, "outputs/group_summary_r.csv", row.names = FALSE)
write.csv(regression_summary, "outputs/regression_summary_r.csv", row.names = FALSE)
write.csv(diagnostic_summary, "outputs/diagnostic_summary_r.csv", row.names = FALSE)
write.csv(claim_summary, "outputs/claim_summary_r.csv", row.names = FALSE)
write.csv(robustness_summary, "outputs/robustness_summary_r.csv", row.names = FALSE)
write.csv(model_summary, "outputs/model_summary_r.csv", row.names = FALSE)

cat("R statistical inference summaries written.\n")
