terraform {
  required_version = ">= 1.6.0"
}

locals {
  warehouse_lake_capabilities = [
    "raw_lake_retention",
    "bronze_silver_gold_layers",
    "dimensional_warehouse_marts",
    "metadata_catalog",
    "lineage_tracking",
    "lakehouse_table_features",
    "schema_on_read_and_write",
    "access_governance",
    "lifecycle_management",
    "cost_performance_monitoring"
  ]
}

output "warehouse_lake_capabilities" {
  value = local.warehouse_lake_capabilities
}
