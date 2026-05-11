#!/usr/bin/env Rscript

# R Workflow: Master Data, Match Confidence, Survivorship, and Stewardship Summary
#
# This workflow summarizes source records, candidate matches, master entities,
# survivorship rules, hierarchy edges, and stewardship review queues.

source_records <- read.csv("data/source_records.csv", stringsAsFactors = FALSE)
candidates <- read.csv("data/candidate_matches.csv", stringsAsFactors = FALSE)
masters <- read.csv("data/master_entities.csv", stringsAsFactors = FALSE)
crosswalk <- read.csv("data/entity_crosswalk.csv", stringsAsFactors = FALSE)
survivorship <- read.csv("data/survivorship_rules.csv", stringsAsFactors = FALSE)
hierarchy <- read.csv("data/hierarchy_edges.csv", stringsAsFactors = FALSE)
stewardship <- read.csv("data/stewardship_queue.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

source_summary <- aggregate(
  record_id ~ source_system + entity_type + domain,
  data = source_records,
  FUN = length
)
names(source_summary) <- c("source_system", "entity_type", "domain", "record_count")

candidate_action_summary <- aggregate(
  candidate_id ~ recommended_action + review_required,
  data = candidates,
  FUN = length
)
names(candidate_action_summary) <- c("recommended_action", "review_required", "candidate_count")

candidate_score_summary <- aggregate(
  match_score ~ entity_type + match_method,
  data = candidates,
  FUN = mean
)
names(candidate_score_summary) <- c("entity_type", "match_method", "average_match_score")

crosswalk_summary <- aggregate(
  confidence ~ master_entity_id + link_status,
  data = crosswalk,
  FUN = mean
)
names(crosswalk_summary) <- c("master_entity_id", "link_status", "average_confidence")

survivorship_summary <- aggregate(
  rule_id ~ entity_type + review_required + conflict_action,
  data = survivorship,
  FUN = length
)
names(survivorship_summary) <- c("entity_type", "review_required", "conflict_action", "rule_count")

stewardship_summary <- aggregate(
  review_id ~ priority + status + review_type,
  data = stewardship,
  FUN = length
)
names(stewardship_summary) <- c("priority", "status", "review_type", "review_count")

hierarchy_summary <- aggregate(
  edge_id ~ relationship_view + relationship_type,
  data = hierarchy,
  FUN = length
)
names(hierarchy_summary) <- c("relationship_view", "relationship_type", "edge_count")

write.csv(source_summary, "outputs/source_summary_r.csv", row.names = FALSE)
write.csv(candidate_action_summary, "outputs/candidate_action_summary_r.csv", row.names = FALSE)
write.csv(candidate_score_summary, "outputs/candidate_score_summary_r.csv", row.names = FALSE)
write.csv(crosswalk_summary, "outputs/crosswalk_summary_r.csv", row.names = FALSE)
write.csv(survivorship_summary, "outputs/survivorship_summary_r.csv", row.names = FALSE)
write.csv(stewardship_summary, "outputs/stewardship_summary_r.csv", row.names = FALSE)
write.csv(hierarchy_summary, "outputs/hierarchy_summary_r.csv", row.names = FALSE)

cat("R MDM and entity-resolution summaries written.\n")
