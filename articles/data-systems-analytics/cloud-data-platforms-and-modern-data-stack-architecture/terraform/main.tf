terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  platform_layers = [
    "source",
    "ingestion",
    "storage",
    "transformation",
    "orchestration",
    "metadata",
    "lineage",
    "semantic",
    "serving",
    "consumption"
  ]
}

output "platform_layers" {
  value = local.platform_layers
}
