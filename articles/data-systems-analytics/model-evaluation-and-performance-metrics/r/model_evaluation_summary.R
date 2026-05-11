#!/usr/bin/env Rscript

# R Workflow: Threshold, Calibration, Classification, and Regression Summary

binary <- read.csv("data/binary_predictions.csv", stringsAsFactors = FALSE)
regression <- read.csv("data/regression_predictions.csv", stringsAsFactors = FALSE)
thresholds <- read.csv("data/threshold_policies.csv", stringsAsFactors = FALSE)
scorecard <- read.csv("data/metric_scorecard.csv", stringsAsFactors = FALSE)
monitoring <- read.csv("data/monitoring_windows.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

safe_div <- function(num, den) {
  ifelse(den == 0, 0, num / den)
}

confusion_metrics <- function(y_true, y_score, threshold) {
  pred <- ifelse(y_score >= threshold, 1, 0)
  tp <- sum(y_true == 1 & pred == 1)
  fp <- sum(y_true == 0 & pred == 1)
  tn <- sum(y_true == 0 & pred == 0)
  fn <- sum(y_true == 1 & pred == 0)
  precision <- safe_div(tp, tp + fp)
  recall <- safe_div(tp, tp + fn)
  accuracy <- safe_div(tp + tn, tp + tn + fp + fn)
  f1 <- safe_div(2 * precision * recall, precision + recall)
  data.frame(
    tp = tp,
    fp = fp,
    tn = tn,
    fn = fn,
    accuracy = accuracy,
    precision = precision,
    recall = recall,
    f1 = f1
  )
}

threshold_rows <- list()
i <- 1
for (model_id in unique(binary$model_id)) {
  rows <- binary[binary$model_id == model_id, ]
  policy_rows <- thresholds[thresholds$model_id == model_id, ]
  for (j in seq_len(nrow(policy_rows))) {
    m <- confusion_metrics(rows$y_true, rows$y_score, policy_rows$threshold[j])
    threshold_rows[[i]] <- cbind(
      model_id = model_id,
      policy_id = policy_rows$policy_id[j],
      threshold = policy_rows$threshold[j],
      policy_name = policy_rows$policy_name[j],
      m
    )
    i <- i + 1
  }
}
threshold_summary <- do.call(rbind, threshold_rows)

calibration_summary <- aggregate(
  cbind(y_true, y_score) ~ model_id,
  data = binary,
  FUN = mean
)
names(calibration_summary) <- c("model_id", "observed_positive_rate", "mean_predicted_score")
calibration_summary$calibration_gap <- abs(
  calibration_summary$observed_positive_rate - calibration_summary$mean_predicted_score
)

regression$absolute_error <- abs(regression$y_pred - regression$y_true)
regression$squared_error <- (regression$y_pred - regression$y_true)^2

regression_summary <- aggregate(
  cbind(absolute_error, squared_error) ~ model_id,
  data = regression,
  FUN = mean
)
names(regression_summary) <- c("model_id", "mae", "mse")
regression_summary$rmse <- sqrt(regression_summary$mse)

monitoring_summary <- aggregate(
  drift_index ~ model_id + status,
  data = monitoring,
  FUN = mean
)
names(monitoring_summary) <- c("model_id", "status", "mean_drift_index")

scorecard_summary <- aggregate(
  observed_value ~ model_id + metric_family + status,
  data = scorecard,
  FUN = length
)
names(scorecard_summary) <- c("model_id", "metric_family", "status", "metric_count")

write.csv(threshold_summary, "outputs/threshold_summary_r.csv", row.names = FALSE)
write.csv(calibration_summary, "outputs/calibration_summary_r.csv", row.names = FALSE)
write.csv(regression_summary, "outputs/regression_summary_r.csv", row.names = FALSE)
write.csv(monitoring_summary, "outputs/monitoring_summary_r.csv", row.names = FALSE)
write.csv(scorecard_summary, "outputs/scorecard_summary_r.csv", row.names = FALSE)

cat("R model evaluation summaries written.\n")
