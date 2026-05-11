terraform {
  required_version = ">= 1.6.0"
}

locals {
  pipeline_processing_capabilities = [
    "ingestion_sources",
    "directed_dataflow_graphs",
    "batch_jobs",
    "stream_processing_jobs",
    "quality_gates",
    "orchestration_dependencies",
    "stateful_processing",
    "replay_and_backfill",
    "idempotency_checks",
    "lineage_and_observability"
  ]
}

output "pipeline_processing_capabilities" {
  value = local.pipeline_processing_capabilities
}
