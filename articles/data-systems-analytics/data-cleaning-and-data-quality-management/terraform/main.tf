terraform {
  required_version = ">= 1.6.0"
}

locals {
  data_quality_capabilities = [
    "raw_record_preservation",
    "quality_rule_registry",
    "profiling_and_validation",
    "deduplication_review",
    "survivorship_rules",
    "rejected_record_quarantine",
    "quality_incident_management",
    "root_cause_register",
    "stewardship_workflows",
    "quality_monitoring"
  ]
}

output "data_quality_capabilities" {
  value = local.data_quality_capabilities
}
