terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  interoperability_capabilities = [
    "api_gateway",
    "schema_registry",
    "message_broker",
    "mapping_registry",
    "entity_crosswalk",
    "lineage_events",
    "quality_observability",
    "access_control"
  ]
}

output "interoperability_capabilities" {
  value = local.interoperability_capabilities
}
