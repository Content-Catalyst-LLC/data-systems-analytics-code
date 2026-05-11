terraform {
  required_version = ">= 1.6.0"
}

# Placeholder only.
# This article scaffold is vendor-neutral and does not create resources.
locals {
  security_privacy_access_capabilities = [
    "classification",
    "iam",
    "policy_engine",
    "secrets_management",
    "masking_tokenization",
    "audit_logging",
    "entitlement_review",
    "retention_management"
  ]
}

output "security_privacy_access_capabilities" {
  value = local.security_privacy_access_capabilities
}
