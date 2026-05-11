terraform {
  required_version = ">= 1.6.0"
}

locals {
  relational_sql_capabilities = [
    "schema_definition",
    "primary_keys",
    "foreign_keys",
    "check_constraints",
    "normalization_review",
    "transaction_management",
    "index_management",
    "query_workload_monitoring",
    "least_privilege_access",
    "backup_and_recovery"
  ]
}

output "relational_sql_capabilities" {
  value = local.relational_sql_capabilities
}
