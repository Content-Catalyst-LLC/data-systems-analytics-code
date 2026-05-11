terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  mdm_entity_resolution_capabilities = [
    "source_registry",
    "candidate_matching",
    "entity_crosswalk",
    "survivorship_rules",
    "stewardship_queue",
    "hierarchy_modeling",
    "external_identifier_linkage",
    "provenance_events",
    "privacy_review"
  ]
}

output "mdm_entity_resolution_capabilities" {
  value = local.mdm_entity_resolution_capabilities
}
