terraform {
  required_version = ">= 1.6.0"
}

locals {
  database_architecture_capabilities = [
    "operational_databases",
    "analytical_databases",
    "object_storage_lakes",
    "streaming_platforms",
    "metadata_catalogs",
    "lineage_tracking",
    "schema_governance",
    "access_controls",
    "backup_and_recovery",
    "lifecycle_management"
  ]
}

output "database_architecture_capabilities" {
  value = local.database_architecture_capabilities
}
