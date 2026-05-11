terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  metadata_catalog_lineage_capabilities = [
    "asset_registry",
    "business_glossary",
    "data_catalog",
    "technical_metadata_harvesting",
    "policy_tags",
    "lineage_edges",
    "provenance_events",
    "quality_signals",
    "usage_metadata"
  ]
}

output "metadata_catalog_lineage_capabilities" {
  value = local.metadata_catalog_lineage_capabilities
}
