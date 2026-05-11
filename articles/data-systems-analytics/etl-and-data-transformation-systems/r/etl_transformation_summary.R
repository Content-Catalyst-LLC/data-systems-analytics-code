#!/usr/bin/env Rscript

# R Workflow: ETL Staging, Mapping, Quality Gates, and Transformation Summary

customers <- read.csv("data/raw_customer_extract.csv", stringsAsFactors = FALSE, na.strings = c("", "NA"))
orders <- read.csv("data/raw_order_extract.csv", stringsAsFactors = FALSE)
mappings <- read.csv("data/status_mapping.csv", stringsAsFactors = FALSE)
tests <- read.csv("data/transformation_tests.csv", stringsAsFactors = FALSE)
runs <- read.csv("data/orchestration_runs.csv", stringsAsFactors = FALSE)
cdc <- read.csv("data/cdc_events.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

customer_mapping <- subset(mappings, canonical_domain == "customer_status")
order_mapping <- subset(mappings, canonical_domain == "order_status")

customers_mapped <- merge(
  customers,
  customer_mapping[, c("source_system", "source_value", "canonical_value", "active_flag")],
  by.x = c("source_system", "status_code"),
  by.y = c("source_system", "source_value"),
  all.x = TRUE
)

customers_mapped$customer_status <- customers_mapped$canonical_value
customers_mapped$email_missing <- ifelse(is.na(customers_mapped$email) | customers_mapped$email == "", 1, 0)

orders_mapped <- merge(
  orders,
  order_mapping[, c("source_system", "source_value", "canonical_value")],
  by.x = c("source_system", "status_code"),
  by.y = c("source_system", "source_value"),
  all.x = TRUE
)

orders_mapped$order_status <- orders_mapped$canonical_value
orders_mapped$amount <- as.numeric(orders_mapped$amount)

customer_summary <- aggregate(
  source_customer_id ~ source_system + customer_status,
  data = customers_mapped,
  FUN = length
)
names(customer_summary) <- c("source_system", "customer_status", "customer_count")

order_summary <- aggregate(
  amount ~ source_system + order_status,
  data = orders_mapped,
  FUN = function(x) c(order_count = length(x), amount_sum = sum(x), amount_mean = mean(x))
)
order_summary <- do.call(data.frame, order_summary)
names(order_summary) <- c("source_system", "order_status", "order_count", "amount_sum", "amount_mean")

quality_summary <- data.frame(
  metric = c(
    "customer_rows",
    "order_rows",
    "missing_customer_email",
    "unmapped_customer_status",
    "unmapped_order_status",
    "negative_completed_order_amount"
  ),
  value = c(
    nrow(customers),
    nrow(orders),
    sum(customers_mapped$email_missing),
    sum(is.na(customers_mapped$customer_status)),
    sum(is.na(orders_mapped$order_status)),
    sum(orders_mapped$order_status == "completed" & orders_mapped$amount < 0, na.rm = TRUE)
  )
)

test_summary <- aggregate(
  test_id ~ scope + status + severity,
  data = tests,
  FUN = length
)
names(test_summary) <- c("scope", "status", "severity", "test_count")

run_summary <- aggregate(
  cbind(input_rows, loaded_rows, rejected_rows) ~ pipeline_name + status,
  data = runs,
  FUN = sum
)

cdc_summary <- aggregate(
  event_id ~ entity + operation,
  data = cdc,
  FUN = length
)
names(cdc_summary) <- c("entity", "operation", "event_count")

write.csv(customer_summary, "outputs/customer_status_summary_r.csv", row.names = FALSE)
write.csv(order_summary, "outputs/order_status_summary_r.csv", row.names = FALSE)
write.csv(quality_summary, "outputs/quality_summary_r.csv", row.names = FALSE)
write.csv(test_summary, "outputs/transformation_test_summary_r.csv", row.names = FALSE)
write.csv(run_summary, "outputs/orchestration_run_summary_r.csv", row.names = FALSE)
write.csv(cdc_summary, "outputs/cdc_summary_r.csv", row.names = FALSE)

cat("R ETL transformation summaries written.\n")
