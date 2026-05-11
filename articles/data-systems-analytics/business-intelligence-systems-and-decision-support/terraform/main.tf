terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  bi_decision_support_capabilities = [
    "metric_catalog",
    "semantic_layer",
    "dashboard_registry",
    "alert_thresholds",
    "decision_review_logs",
    "access_control",
    "lineage",
    "quality_observability"
  ]
}

output "bi_decision_support_capabilities" {
  value = local.bi_decision_support_capabilities
}
