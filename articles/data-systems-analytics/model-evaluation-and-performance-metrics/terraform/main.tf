terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  model_evaluation_capabilities = [
    "model_registry",
    "binary_predictions",
    "regression_predictions",
    "threshold_policies",
    "metric_scorecard",
    "calibration_review",
    "subgroup_evaluation",
    "monitoring_windows",
    "governance_limits"
  ]
}

output "model_evaluation_capabilities" {
  value = local.model_evaluation_capabilities
}
