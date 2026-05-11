# Data Lifecycle Management and Retention
# R workflow: analyze data aging, access patterns, retention risk, storage exposure,
# ownership gaps, legal holds, and lifecycle status.

suppressPackageStartupMessages({
  library(tidyverse)
  library(lubridate)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- "--file="
script_path <- sub(file_arg, "", args[grepl(file_arg, args)][1])

if (!is.na(script_path) && file.exists(script_path)) {
  base_dir <- normalizePath(file.path(dirname(script_path), ".."), mustWork = FALSE)
} else {
  base_dir <- getwd()
}

if (!dir.exists(file.path(base_dir, "data"))) {
  base_dir <- normalizePath(file.path(getwd()), mustWork = FALSE)
}

data_dir <- file.path(base_dir, "data")
output_dir <- file.path(base_dir, "outputs")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

today <- as.Date("2026-03-31")

assets <- read_csv(
  file.path(data_dir, "retention_assets.csv"),
  show_col_types = FALSE
) %>%
  mutate(
    created_date = as.Date(created_date),
    trigger_date = as.Date(trigger_date),
    last_accessed_date = as.Date(last_accessed_date),
    legal_hold = as.logical(legal_hold),
    owner = replace_na(owner, "")
  )

rules <- read_csv(
  file.path(data_dir, "retention_rules.csv"),
  show_col_types = FALSE
) %>%
  mutate(
    requires_archival_review = as.logical(requires_archival_review)
  )

asset_risk <- assets %>%
  left_join(rules, by = "retention_category") %>%
  mutate(
    expiration_date = trigger_date %m+% years(retention_years),
    asset_age_days = as.integer(today - created_date),
    inactive_days = as.integer(today - last_accessed_date),
    retention_expired = today > expiration_date,
    ownership_gap = is.na(owner) | owner == "",
    sensitive = classification %in% c(
      "personal_data",
      "sensitive_personal_data",
      "derived_personal_data",
      "behavioral_log"
    ),
    high_reuse = downstream_dependencies >= 5,
    high_storage = storage_gb > 50,
    lifecycle_risk_score =
      2 * as.integer(retention_expired) +
      2 * as.integer(sensitive) +
      2 * as.integer(ownership_gap) +
      1 * as.integer(inactive_days > 365) +
      1 * as.integer(high_storage) +
      1 * as.integer(high_reuse) +
      3 * as.integer(legal_hold),
    lifecycle_status = case_when(
      legal_hold ~ "retain_legal_hold",
      retention_expired & archival_value == "high" ~ "archive_review_required",
      retention_expired & downstream_dependencies > 0 ~ "dependency_review_required",
      retention_expired ~ "eligible_for_disposition",
      ownership_gap ~ "assign_owner",
      inactive_days > 365 & archival_value == "low" ~ "inactive_review",
      TRUE ~ "active_retain"
    )
  )

system_summary <- asset_risk %>%
  group_by(system) %>%
  summarise(
    asset_count = n(),
    total_storage_gb = sum(storage_gb),
    expired_assets = sum(retention_expired),
    sensitive_assets = sum(sensitive),
    ownership_gaps = sum(ownership_gap),
    legal_holds = sum(legal_hold),
    average_lifecycle_risk_score = mean(lifecycle_risk_score),
    .groups = "drop"
  ) %>%
  arrange(desc(average_lifecycle_risk_score), desc(total_storage_gb))

action_register <- asset_risk %>%
  filter(lifecycle_status != "active_retain") %>%
  transmute(
    asset_id,
    system,
    owner,
    classification,
    retention_category,
    lifecycle_status,
    recommended_action = case_when(
      lifecycle_status == "retain_legal_hold" ~ "Preserve until legal hold is released and reviewed",
      lifecycle_status == "archive_review_required" ~ "Review for long-term archival preservation and access restrictions",
      lifecycle_status == "dependency_review_required" ~ "Review lineage and downstream dependencies before disposition",
      lifecycle_status == "eligible_for_disposition" ~ "Approve deletion, anonymization, or secure sanitization",
      lifecycle_status == "assign_owner" ~ "Assign accountable owner before lifecycle decision",
      lifecycle_status == "inactive_review" ~ "Review inactive asset for archive, restriction, or disposal",
      TRUE ~ "Review required"
    )
  )

avoidable_storage <- asset_risk %>%
  filter(
    lifecycle_status %in% c(
      "eligible_for_disposition",
      "inactive_review",
      "dependency_review_required"
    )
  ) %>%
  summarise(
    candidate_asset_count = n(),
    candidate_storage_gb = sum(storage_gb),
    sensitive_candidate_assets = sum(sensitive)
  )

governance_scorecard <- asset_risk %>%
  summarise(
    total_assets = n(),
    expired_assets = sum(retention_expired),
    assets_under_legal_hold = sum(legal_hold),
    assets_with_ownership_gaps = sum(ownership_gap),
    inactive_assets = sum(inactive_days > 365),
    sensitive_assets = sum(sensitive),
    total_storage_gb = sum(storage_gb),
    storage_gb_in_review = sum(storage_gb[lifecycle_status != "active_retain"])
  )

write_csv(asset_risk, file.path(output_dir, "r_lifecycle_asset_risk.csv"))
write_csv(system_summary, file.path(output_dir, "r_system_summary.csv"))
write_csv(action_register, file.path(output_dir, "r_action_register.csv"))
write_csv(avoidable_storage, file.path(output_dir, "r_avoidable_storage.csv"))
write_csv(governance_scorecard, file.path(output_dir, "r_governance_scorecard.csv"))

print(asset_risk)
print(system_summary)
print(action_register)
print(avoidable_storage)
print(governance_scorecard)
