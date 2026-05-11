terraform {
  required_version = ">= 1.6.0"
}

locals {
  forecasting_capabilities = [
    "time_series_observations",
    "forecast_model_registry",
    "diagnostic_checks",
    "rolling_origin_backtests",
    "forecast_horizons",
    "prediction_intervals",
    "forecast_monitoring"
  ]
}

output "forecasting_capabilities" {
  value = local.forecasting_capabilities
}
