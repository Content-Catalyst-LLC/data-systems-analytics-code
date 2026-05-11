terraform {
  required_version = ">= 1.6.0"
}

locals {
  streaming_analytics_capabilities = [
    "event_topics",
    "schema_registry",
    "event_time_windows",
    "watermarks",
    "stateful_aggregates",
    "alert_rules",
    "serving_views",
    "replay_and_reconstruction",
    "streaming_governance_review"
  ]
}

output "streaming_analytics_capabilities" {
  value = local.streaming_analytics_capabilities
}
