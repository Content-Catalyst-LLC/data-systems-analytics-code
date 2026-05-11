terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  governance_stewardship_capabilities = [
    "asset_registry",
    "stewardship_roles",
    "decision_rights",
    "policy_register",
    "quality_issue_queue",
    "access_reviews",
    "lifecycle_controls",
    "responsible_use_reviews",
    "governance_events"
  ]
}

output "governance_stewardship_capabilities" {
  value = local.governance_stewardship_capabilities
}
