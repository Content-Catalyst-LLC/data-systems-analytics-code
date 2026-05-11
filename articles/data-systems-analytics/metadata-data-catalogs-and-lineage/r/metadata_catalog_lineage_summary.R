#!/usr/bin/env Rscript

# R Workflow: Metadata, Catalog, Lineage, Policy, and Usage Summary
#
# This workflow summarizes metadata coverage, catalog trust signals,
# glossary alignment, lineage granularity, policy enforcement, and usage.

assets <- read.csv("data/data_assets.csv", stringsAsFactors = FALSE)
metadata <- read.csv("data/metadata_elements.csv", stringsAsFactors = FALSE)
catalog <- read.csv("data/catalog_entries.csv", stringsAsFactors = FALSE)
glossary <- read.csv("data/glossary_terms.csv", stringsAsFactors = FALSE)
lineage <- read.csv("data/lineage_edges.csv", stringsAsFactors = FALSE)
policies <- read.csv("data/policy_tags.csv", stringsAsFactors = FALSE)
signals <- read.csv("data/quality_signals.csv", stringsAsFactors = FALSE)
usage <- read.csv("data/catalog_usage.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

asset_summary <- aggregate(
  asset_id ~ domain + asset_type + certification_status,
  data = assets,
  FUN = length
)
names(asset_summary) <- c("domain", "asset_type", "certification_status", "asset_count")

metadata_type_summary <- aggregate(
  metadata_id ~ metadata_type + quality_status,
  data = metadata,
  FUN = length
)
names(metadata_type_summary) <- c("metadata_type", "quality_status", "element_count")

catalog_trust_summary <- aggregate(
  catalog_entry_id ~ trust_label,
  data = catalog,
  FUN = length
)
names(catalog_trust_summary) <- c("trust_label", "catalog_entry_count")

glossary_summary <- aggregate(
  term_id ~ domain + certification_status,
  data = glossary,
  FUN = length
)
names(glossary_summary) <- c("domain", "certification_status", "term_count")

lineage_summary <- aggregate(
  edge_id ~ relationship_type + lineage_granularity + impact_level,
  data = lineage,
  FUN = length
)
names(lineage_summary) <- c("relationship_type", "lineage_granularity", "impact_level", "edge_count")

policy_summary <- aggregate(
  policy_tag_id ~ tag_type + enforcement_status,
  data = policies,
  FUN = length
)
names(policy_summary) <- c("tag_type", "enforcement_status", "policy_tag_count")

quality_signal_summary <- aggregate(
  signal_id ~ signal_type + status + severity,
  data = signals,
  FUN = length
)
names(quality_signal_summary) <- c("signal_type", "status", "severity", "signal_count")

usage$total_activity <- usage$search_count + usage$view_count + usage$query_count

write.csv(asset_summary, "outputs/asset_summary_r.csv", row.names = FALSE)
write.csv(metadata_type_summary, "outputs/metadata_type_summary_r.csv", row.names = FALSE)
write.csv(catalog_trust_summary, "outputs/catalog_trust_summary_r.csv", row.names = FALSE)
write.csv(glossary_summary, "outputs/glossary_summary_r.csv", row.names = FALSE)
write.csv(lineage_summary, "outputs/lineage_summary_r.csv", row.names = FALSE)
write.csv(policy_summary, "outputs/policy_summary_r.csv", row.names = FALSE)
write.csv(quality_signal_summary, "outputs/quality_signal_summary_r.csv", row.names = FALSE)
write.csv(usage, "outputs/catalog_usage_summary_r.csv", row.names = FALSE)

cat("R metadata, catalog, and lineage summaries written.\n")
