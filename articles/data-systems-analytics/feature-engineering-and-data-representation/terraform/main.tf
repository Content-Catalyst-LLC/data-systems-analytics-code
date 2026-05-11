terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  feature_engineering_capabilities = [
    "feature_registry",
    "transformation_rules",
    "feature_quality_checks",
    "feature_selection",
    "representation_metrics",
    "leakage_review",
    "training_inference_parity",
    "feature_lineage",
    "governance_review"
  ]
}

output "feature_engineering_capabilities" {
  value = local.feature_engineering_capabilities
}
