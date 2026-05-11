terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  dashboard_storytelling_capabilities = [
    "dashboard_inventory",
    "kpi_definitions",
    "filter_controls",
    "linked_views",
    "story_points",
    "annotations",
    "interaction_events",
    "accessibility_checks",
    "governance_checks",
    "evidence_links"
  ]
}

output "dashboard_storytelling_capabilities" {
  value = local.dashboard_storytelling_capabilities
}
