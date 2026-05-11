#!/usr/bin/env Rscript

# R Workflow: Descriptive Analytics, Missingness, Subgroup Summaries, and EDA Checks

records <- read.csv("data/exploration_dataset.csv", stringsAsFactors = FALSE, na.strings = c("NA", ""))
checks <- read.csv("data/exploration_checks.csv", stringsAsFactors = FALSE)
questions <- read.csv("data/exploration_questions.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

numeric_vars <- c("value", "volume", "quality_score", "response_time")

numeric_summary <- data.frame()
for (var in numeric_vars) {
  x <- records[[var]]
  numeric_summary <- rbind(
    numeric_summary,
    data.frame(
      variable_name = var,
      n = length(x),
      non_missing = sum(!is.na(x)),
      missing = sum(is.na(x)),
      missing_rate = mean(is.na(x)),
      mean = mean(x, na.rm = TRUE),
      median = median(x, na.rm = TRUE),
      sd = sd(x, na.rm = TRUE),
      min = min(x, na.rm = TRUE),
      q1 = quantile(x, 0.25, na.rm = TRUE),
      q3 = quantile(x, 0.75, na.rm = TRUE),
      max = max(x, na.rm = TRUE)
    )
  )
}

subgroup_summary <- aggregate(
  value ~ segment + region,
  data = records,
  FUN = function(x) c(n = length(x), mean = mean(x, na.rm = TRUE), median = median(x, na.rm = TRUE))
)
subgroup_summary <- do.call(data.frame, subgroup_summary)
names(subgroup_summary) <- c("segment", "region", "n", "mean_value", "median_value")

missingness <- aggregate(
  missing_flag ~ segment + region,
  data = records,
  FUN = mean
)
names(missingness) <- c("segment", "region", "missing_value_rate")

category_summary <- as.data.frame(table(records$segment, records$region))
names(category_summary) <- c("segment", "region", "count")

relationship_summary <- data.frame(
  left_variable = c("value", "value", "value", "volume"),
  right_variable = c("volume", "quality_score", "response_time", "quality_score"),
  correlation = c(
    cor(records$value, records$volume, use = "complete.obs"),
    cor(records$value, records$quality_score, use = "complete.obs"),
    cor(records$value, records$response_time, use = "complete.obs"),
    cor(records$volume, records$quality_score, use = "complete.obs")
  )
)

check_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = checks,
  FUN = length
)
names(check_summary) <- c("check_type", "status", "severity", "check_count")

question_summary <- aggregate(
  question_id ~ analysis_mode + priority + status,
  data = questions,
  FUN = length
)
names(question_summary) <- c("analysis_mode", "priority", "status", "question_count")

write.csv(numeric_summary, "outputs/numeric_summary_r.csv", row.names = FALSE)
write.csv(subgroup_summary, "outputs/subgroup_summary_r.csv", row.names = FALSE)
write.csv(missingness, "outputs/missingness_summary_r.csv", row.names = FALSE)
write.csv(category_summary, "outputs/category_summary_r.csv", row.names = FALSE)
write.csv(relationship_summary, "outputs/relationship_summary_r.csv", row.names = FALSE)
write.csv(check_summary, "outputs/exploration_check_summary_r.csv", row.names = FALSE)
write.csv(question_summary, "outputs/exploration_question_summary_r.csv", row.names = FALSE)

cat("R descriptive analytics and EDA summaries written.\n")
