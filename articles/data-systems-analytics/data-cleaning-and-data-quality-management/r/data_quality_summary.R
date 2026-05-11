#!/usr/bin/env Rscript

# R Workflow: Data Quality Dimensions, Profiling, Rule Results, and Stewardship Summary

records <- read.csv("data/raw_customer_records.csv", stringsAsFactors = FALSE, na.strings = c("", "NA"))
rules <- read.csv("data/quality_rules.csv", stringsAsFactors = FALSE)
mapping <- read.csv("data/status_mapping.csv", stringsAsFactors = FALSE)
root_causes <- read.csv("data/root_cause_register.csv", stringsAsFactors = FALSE)
incidents <- read.csv("data/quality_incidents.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

records$email_normalized <- tolower(trimws(records$email))
records$country_standardized <- ifelse(records$country_code %in% c("US", "USA"), "US", records$country_code)
records$lifetime_value <- as.numeric(records$lifetime_value)
records$email_present <- ifelse(is.na(records$email_normalized) | records$email_normalized == "", 0, 1)
records$email_valid <- ifelse(grepl("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", records$email_normalized), 1, 0)
records$value_nonnegative <- ifelse(!is.na(records$lifetime_value) & records$lifetime_value >= 0, 1, 0)
records$country_valid <- ifelse(records$country_code %in% c("US", "USA"), 1, 0)
records$signup_date_valid <- ifelse(is.na(as.Date(records$signup_date, format = "%Y-%m-%d")), 0, 1)

email_counts <- table(records$email_normalized)
records$duplicate_email_flag <- ifelse(!is.na(records$email_normalized) & records$email_normalized != "" & email_counts[records$email_normalized] > 1, 1, 0)

profile_summary <- data.frame(
  metric = c(
    "row_count",
    "email_completeness",
    "email_validity",
    "signup_date_validity",
    "lifetime_value_nonnegative",
    "country_code_validity",
    "duplicate_email_rate"
  ),
  value = c(
    nrow(records),
    mean(records$email_present),
    mean(records$email_valid, na.rm = TRUE),
    mean(records$signup_date_valid),
    mean(records$value_nonnegative, na.rm = TRUE),
    mean(records$country_valid),
    mean(records$duplicate_email_flag)
  )
)

source_summary <- aggregate(
  record_id ~ source_system + status,
  data = records,
  FUN = length
)
names(source_summary) <- c("source_system", "status", "record_count")

quality_by_source <- aggregate(
  cbind(email_present, email_valid, value_nonnegative, duplicate_email_flag) ~ source_system,
  data = records,
  FUN = mean,
  na.rm = TRUE
)

rule_summary <- aggregate(
  rule_id ~ dimension + severity + status,
  data = rules,
  FUN = length
)
names(rule_summary) <- c("dimension", "severity", "status", "rule_count")

incident_summary <- aggregate(
  incident_id ~ rule_id + incident_status + affected_metric,
  data = incidents,
  FUN = length
)
names(incident_summary) <- c("rule_id", "incident_status", "affected_metric", "incident_count")

root_cause_summary <- aggregate(
  issue_id ~ quality_dimension + affected_system + remediation_status,
  data = root_causes,
  FUN = length
)
names(root_cause_summary) <- c("quality_dimension", "affected_system", "remediation_status", "issue_count")

write.csv(profile_summary, "outputs/profile_summary_r.csv", row.names = FALSE)
write.csv(source_summary, "outputs/source_status_summary_r.csv", row.names = FALSE)
write.csv(quality_by_source, "outputs/quality_by_source_r.csv", row.names = FALSE)
write.csv(rule_summary, "outputs/quality_rule_summary_r.csv", row.names = FALSE)
write.csv(incident_summary, "outputs/quality_incident_summary_r.csv", row.names = FALSE)
write.csv(root_cause_summary, "outputs/root_cause_summary_r.csv", row.names = FALSE)

cat("R data quality summaries written.\n")
