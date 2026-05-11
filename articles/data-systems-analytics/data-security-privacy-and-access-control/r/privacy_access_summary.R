#!/usr/bin/env Rscript

# R Workflow: Security Classification, Privacy Purpose, and Access Review Summary
#
# This workflow summarizes asset classification, entitlement status,
# privacy purpose approval, and audit anomalies using base R.

assets <- read.csv("data/data_assets.csv", stringsAsFactors = FALSE)
policies <- read.csv("data/access_policies.csv", stringsAsFactors = FALSE)
entitlements <- read.csv("data/entitlements.csv", stringsAsFactors = FALSE)
purposes <- read.csv("data/privacy_purposes.csv", stringsAsFactors = FALSE)
audits <- read.csv("data/audit_events.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

classification_summary <- aggregate(
  asset_id ~ classification + contains_personal_data,
  data = assets,
  FUN = length
)
names(classification_summary) <- c("classification", "contains_personal_data", "asset_count")

policy_summary <- aggregate(
  policy_id ~ decision + access_type,
  data = policies,
  FUN = length
)
names(policy_summary) <- c("decision", "access_type", "policy_count")

entitlement_summary <- aggregate(
  entitlement_id ~ status + temporary_exception,
  data = entitlements,
  FUN = length
)
names(entitlement_summary) <- c("status", "temporary_exception", "entitlement_count")

purpose_summary <- aggregate(
  purpose_id ~ status + minimized_fields + retention_aligned,
  data = purposes,
  FUN = length
)
names(purpose_summary) <- c("status", "minimized_fields", "retention_aligned", "purpose_count")

audit_summary <- aggregate(
  event_id ~ decision + anomaly_flag,
  data = audits,
  FUN = length
)
names(audit_summary) <- c("decision", "anomaly_flag", "event_count")

write.csv(classification_summary, "outputs/classification_summary_r.csv", row.names = FALSE)
write.csv(policy_summary, "outputs/policy_summary_r.csv", row.names = FALSE)
write.csv(entitlement_summary, "outputs/entitlement_summary_r.csv", row.names = FALSE)
write.csv(purpose_summary, "outputs/privacy_purpose_summary_r.csv", row.names = FALSE)
write.csv(audit_summary, "outputs/audit_event_summary_r.csv", row.names = FALSE)

cat("R security, privacy, and access review outputs written.\n")
