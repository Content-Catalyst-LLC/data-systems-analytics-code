# Data Systems & Analytics R workflow.
# Run from repository root:
# Rscript r/analytics_summary.R

observations <- read.csv("data/raw/observations.csv", stringsAsFactors = FALSE)
entities <- read.csv("data/raw/entities.csv", stringsAsFactors = FALSE)

observations$metric_value <- as.numeric(observations$metric_value)
joined <- merge(observations, entities, by = "system_id", all.x = TRUE)

summary_table <- aggregate(
  metric_value ~ domain + system_name + metric_name + unit,
  data = joined,
  FUN = function(x) c(n = length(x), mean = mean(x), min = min(x), max = max(x))
)

expanded <- data.frame(
  domain = summary_table$domain,
  system_name = summary_table$system_name,
  metric_name = summary_table$metric_name,
  unit = summary_table$unit,
  n = summary_table$metric_value[, "n"],
  mean = round(summary_table$metric_value[, "mean"], 4),
  min = round(summary_table$metric_value[, "min"], 4),
  max = round(summary_table$metric_value[, "max"], 4)
)

dir.create("outputs", showWarnings = FALSE)
write.csv(expanded, "outputs/r-metric-summary.csv", row.names = FALSE)

png("outputs/r-metric-summary.png", width = 1200, height = 800)
barplot(
  expanded$mean,
  names.arg = expanded$system_name,
  las = 2,
  main = "Average Metric Value by System",
  ylab = "Average Metric Value"
)
dev.off()

cat("Wrote outputs/r-metric-summary.csv and outputs/r-metric-summary.png\n")
