terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  quality_observability_capabilities = [
    "quality_checks",
    "freshness_monitoring",
    "volume_monitoring",
    "schema_drift_detection",
    "distribution_drift_detection",
    "lineage_impact",
    "incident_response",
    "remediation_metrics"
  ]
}

output "quality_observability_capabilities" {
  value = local.quality_observability_capabilities
}
