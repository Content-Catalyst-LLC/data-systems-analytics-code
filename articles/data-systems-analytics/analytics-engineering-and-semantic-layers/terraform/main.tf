terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  semantic_layer_capabilities = [
    "model_registry",
    "semantic_metrics",
    "metric_api",
    "catalog",
    "lineage",
    "test_results",
    "definition_drift_review",
    "access_rules"
  ]
}

output "semantic_layer_capabilities" {
  value = local.semantic_layer_capabilities
}
