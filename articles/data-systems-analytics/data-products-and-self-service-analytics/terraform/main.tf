terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  data_product_capabilities = [
    "catalog",
    "semantic_layer",
    "quality_checks",
    "lineage",
    "access_control",
    "usage_monitoring",
    "lifecycle_management"
  ]
}

output "data_product_capabilities" {
  value = local.data_product_capabilities
}
