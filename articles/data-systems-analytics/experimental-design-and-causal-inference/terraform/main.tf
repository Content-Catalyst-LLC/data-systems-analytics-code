terraform {
  required_version = ">= 1.6.0"
}

locals {
  causal_evidence_capabilities = [
    "causal_study_registry",
    "assignment_records",
    "outcome_records",
    "assumption_checks",
    "estimand_registry",
    "robustness_outputs",
    "governance_review"
  ]
}

output "causal_evidence_capabilities" {
  value = local.causal_evidence_capabilities
}
