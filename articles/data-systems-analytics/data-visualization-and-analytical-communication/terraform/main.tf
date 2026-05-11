terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  visualization_communication_capabilities = [
    "visualization_inventory",
    "chart_assessments",
    "encoding_assessments",
    "uncertainty_elements",
    "annotation_elements",
    "accessibility_checks",
    "evidence_links",
    "audience_contexts",
    "review_checkpoints",
    "visual_outputs"
  ]
}

output "visualization_communication_capabilities" {
  value = local.visualization_communication_capabilities
}
