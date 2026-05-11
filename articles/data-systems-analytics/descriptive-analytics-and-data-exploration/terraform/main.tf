terraform {
  required_version = ">= 1.6.0"
}

locals {
  descriptive_eda_capabilities = [
    "dataset_profile",
    "numeric_distribution_summary",
    "categorical_frequency_summary",
    "missingness_profile",
    "subgroup_summary",
    "outlier_review",
    "exploration_question_registry",
    "eda_governance_review"
  ]
}

output "descriptive_eda_capabilities" {
  value = local.descriptive_eda_capabilities
}
