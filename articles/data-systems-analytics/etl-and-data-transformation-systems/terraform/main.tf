terraform {
  required_version = ">= 1.6.0"
}

locals {
  etl_transformation_capabilities = [
    "raw_extract_landing",
    "staging_tables",
    "semantic_mapping_registry",
    "canonical_target_models",
    "quality_gates",
    "idempotent_merge_logic",
    "cdc_change_events",
    "lineage_records",
    "rejected_record_quarantine",
    "orchestration_monitoring"
  ]
}

output "etl_transformation_capabilities" {
  value = local.etl_transformation_capabilities
}
