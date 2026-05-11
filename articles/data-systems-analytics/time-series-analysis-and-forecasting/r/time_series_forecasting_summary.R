#!/usr/bin/env Rscript

# R Workflow: Time Series Diagnostics, Backtesting, and Forecast Governance Summary

observations <- read.csv("data/monthly_demand.csv", stringsAsFactors = FALSE)
registry <- read.csv("data/forecast_model_registry.csv", stringsAsFactors = FALSE)
backtests <- read.csv("data/backtest_windows.csv", stringsAsFactors = FALSE)
checks <- read.csv("data/diagnostic_checks.csv", stringsAsFactors = FALSE)
horizons <- read.csv("data/forecast_horizons.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

model_summary <- aggregate(
  model_id ~ model_family + validation_design + status + risk_level,
  data = registry,
  FUN = length
)
names(model_summary) <- c("model_family", "validation_design", "status", "risk_level", "model_count")

backtests$error <- backtests$actual - backtests$forecast
backtests$absolute_error <- abs(backtests$error)
backtests$squared_error <- backtests$error ^ 2
backtests$interval_hit_80 <- ifelse(backtests$actual >= backtests$lower_80 & backtests$actual <= backtests$upper_80, 1, 0)

backtest_summary <- aggregate(
  cbind(absolute_error, squared_error, interval_hit_80) ~ model_id + horizon,
  data = backtests,
  FUN = mean
)
names(backtest_summary) <- c("model_id", "horizon", "mae", "mean_squared_error", "interval_coverage_80")
backtest_summary$rmse <- sqrt(backtest_summary$mean_squared_error)

check_summary <- aggregate(
  check_id ~ check_type + status + severity,
  data = checks,
  FUN = length
)
names(check_summary) <- c("check_type", "status", "severity", "check_count")

horizons$width_80 <- horizons$upper_80 - horizons$lower_80
horizons$width_95 <- horizons$upper_95 - horizons$lower_95

horizon_summary <- aggregate(
  cbind(width_80, width_95) ~ model_id + horizon + release_status,
  data = horizons,
  FUN = mean
)

observations$year <- substr(observations$date, 1, 4)
year_summary <- aggregate(
  value ~ series_id + year,
  data = observations,
  FUN = mean
)
names(year_summary) <- c("series_id", "year", "mean_value")

write.csv(model_summary, "outputs/model_summary_r.csv", row.names = FALSE)
write.csv(backtest_summary, "outputs/backtest_summary_r.csv", row.names = FALSE)
write.csv(check_summary, "outputs/diagnostic_check_summary_r.csv", row.names = FALSE)
write.csv(horizon_summary, "outputs/horizon_interval_summary_r.csv", row.names = FALSE)
write.csv(year_summary, "outputs/year_summary_r.csv", row.names = FALSE)

cat("R time-series forecasting summaries written.\n")
