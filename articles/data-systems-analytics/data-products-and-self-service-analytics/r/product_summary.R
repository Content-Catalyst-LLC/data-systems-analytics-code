#!/usr/bin/env Rscript

products <- read.csv("data/data_products.csv", stringsAsFactors = FALSE)
access <- read.csv("data/access_events.csv", stringsAsFactors = FALSE)

dir.create("outputs", showWarnings = FALSE, recursive = TRUE)

domain_summary <- aggregate(
  product_id ~ domain,
  data = products,
  FUN = length
)
names(domain_summary) <- c("domain", "product_count")
write.csv(domain_summary, "outputs/domain_summary_r.csv", row.names = FALSE)

lifecycle_summary <- aggregate(
  product_id ~ lifecycle_status,
  data = products,
  FUN = length
)
names(lifecycle_summary) <- c("lifecycle_status", "product_count")
write.csv(lifecycle_summary, "outputs/lifecycle_summary_r.csv", row.names = FALSE)

usage_summary <- aggregate(
  cbind(dashboard_views, notebook_sessions, api_calls, ad_hoc_queries) ~ product_id,
  data = access,
  FUN = sum
)
write.csv(usage_summary, "outputs/usage_summary_r.csv", row.names = FALSE)

cat("R data product summary complete\n")
