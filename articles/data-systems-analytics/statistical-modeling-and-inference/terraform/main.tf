terraform {
  required_version = ">= 1.6.0"
}

locals {
  statistical_inference_capabilities = [
    "sample_observations",
    "model_registry",
    "inference_claims",
    "diagnostic_checks",
    "robustness_checks",
    "uncertainty_records",
    "governance_review"
  ]
}

output "statistical_inference_capabilities" {
  value = local.statistical_inference_capabilities
}
