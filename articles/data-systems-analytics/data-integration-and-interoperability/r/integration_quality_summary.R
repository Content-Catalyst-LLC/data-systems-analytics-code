#!/usr/bin/env Rscript

# R Workflow: Integration Coverage and Interoperability Quality Summary
#
# This workflow summarizes mapping coverage, semantic risk, interoperability
# check status, and entity-crosswalk confidence using base R.

systems <- read.csv("data/source_systems.csv", stringsAsFactors = FALSE)
mappings <- read.csv("data/schema_mappings.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/interoperability_checks.csv", stringsAsFactors = FALSE)
crosswalk <- read.csv("data/entity_crosswalk.csv", stringsAsFactors = FALSE)
payloads <- read.csv("data/message_payloads.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

system_summary <- aggregate(
  system_id ~ domain + system_type,
  data = systems,
  FUN = length
)
names(system_summary) <- c("domain", "system_type", "system_count")

mapping_risk <- aggregate(
  mapping_id ~ semantic_risk + status,
  data = mappings,
  FUN = length
)
names(mapping_risk) <- c("semantic_risk", "status", "mapping_count")

check_summary <- aggregate(
  check_id ~ layer + status,
  data = checks,
  FUN = length
)
names(check_summary) <- c("layer", "status", "check_count")

crosswalk_summary <- aggregate(
  confidence ~ entity_type + match_method,
  data = crosswalk,
  FUN = mean
)
names(crosswalk_summary) <- c("entity_type", "match_method", "average_confidence")

payload_readiness <- data.frame(
  total_payloads = nrow(payloads),
  syntax_valid = sum(payloads$syntax_valid == "true"),
  semantic_valid = sum(payloads$semantic_valid == "true"),
  minimized_payloads = sum(payloads$minimized_payload == "true"),
  consumer_ready = sum(payloads$consumer_ready == "true")
)

write.csv(system_summary, "outputs/system_summary_r.csv", row.names = FALSE)
write.csv(mapping_risk, "outputs/mapping_risk_summary_r.csv", row.names = FALSE)
write.csv(check_summary, "outputs/interoperability_check_summary_r.csv", row.names = FALSE)
write.csv(crosswalk_summary, "outputs/entity_crosswalk_summary_r.csv", row.names = FALSE)
write.csv(payload_readiness, "outputs/payload_readiness_r.csv", row.names = FALSE)

cat("R integration coverage and interoperability quality outputs written.\n")
