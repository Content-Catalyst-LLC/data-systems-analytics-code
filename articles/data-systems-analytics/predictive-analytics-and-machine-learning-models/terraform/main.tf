terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  predictive_analytics_capabilities = [
    "model_registry",
    "classification_predictions",
    "regression_predictions",
    "training_validation_splits",
    "threshold_policies",
    "metric_scorecard",
    "leakage_shift_checks",
    "monitoring_windows",
    "predictive_governance"
  ]
}

output "predictive_analytics_capabilities" {
  value = local.predictive_analytics_capabilities
}
