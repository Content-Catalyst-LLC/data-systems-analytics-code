#!/usr/bin/env Rscript

# R Workflow: Governance Roles, Policies, Quality, Access, Lifecycle, and Risk Summary

assets <- read.csv("data/data_assets.csv", stringsAsFactors = FALSE)
roles <- read.csv("data/stewardship_roles.csv", stringsAsFactors = FALSE)
decisions <- read.csv("data/decision_rights.csv", stringsAsFactors = FALSE)
policies <- read.csv("data/policy_register.csv", stringsAsFactors = FALSE)
issues <- read.csv("data/quality_issues.csv", stringsAsFactors = FALSE)
access <- read.csv("data/access_reviews.csv", stringsAsFactors = FALSE)
lifecycle <- read.csv("data/lifecycle_controls.csv", stringsAsFactors = FALSE)
risks <- read.csv("data/responsible_use_risks.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

asset_summary <- aggregate(
  asset_id ~ domain + classification + certification_status + lifecycle_status,
  data = assets,
  FUN = length
)
names(asset_summary) <- c("domain", "classification", "certification_status", "lifecycle_status", "asset_count")

role_summary <- aggregate(
  role_id ~ domain + role_type + active,
  data = roles,
  FUN = length
)
names(role_summary) <- c("domain", "role_type", "active", "role_count")

decision_summary <- aggregate(
  decision_id ~ domain + decision_area + approver_role,
  data = decisions,
  FUN = length
)
names(decision_summary) <- c("domain", "decision_area", "approver_role", "decision_count")

policy_summary <- aggregate(
  policy_id ~ policy_domain + policy_type + enforcement_status,
  data = policies,
  FUN = length
)
names(policy_summary) <- c("policy_domain", "policy_type", "enforcement_status", "policy_count")

issue_summary <- aggregate(
  issue_id ~ severity + status + assigned_steward,
  data = issues,
  FUN = length
)
names(issue_summary) <- c("severity", "status", "assigned_steward", "issue_count")

access_summary <- aggregate(
  access_id ~ risk_level + decision + approver_role,
  data = access,
  FUN = length
)
names(access_summary) <- c("risk_level", "decision", "approver_role", "access_count")

lifecycle_summary <- aggregate(
  control_id ~ lifecycle_stage + control_type + status,
  data = lifecycle,
  FUN = length
)
names(lifecycle_summary) <- c("lifecycle_stage", "control_type", "status", "control_count")

risk_summary <- aggregate(
  risk_id ~ risk_type + severity + review_status,
  data = risks,
  FUN = length
)
names(risk_summary) <- c("risk_type", "severity", "review_status", "risk_count")

write.csv(asset_summary, "outputs/asset_summary_r.csv", row.names = FALSE)
write.csv(role_summary, "outputs/role_summary_r.csv", row.names = FALSE)
write.csv(decision_summary, "outputs/decision_rights_summary_r.csv", row.names = FALSE)
write.csv(policy_summary, "outputs/policy_summary_r.csv", row.names = FALSE)
write.csv(issue_summary, "outputs/quality_issue_summary_r.csv", row.names = FALSE)
write.csv(access_summary, "outputs/access_review_summary_r.csv", row.names = FALSE)
write.csv(lifecycle_summary, "outputs/lifecycle_control_summary_r.csv", row.names = FALSE)
write.csv(risk_summary, "outputs/responsible_use_risk_summary_r.csv", row.names = FALSE)

cat("R governance and stewardship summaries written.\n")
