# Descriptive Analytics and Data Exploration

This companion code models descriptive analytics and EDA as evidence infrastructure: dataset profiling, missingness, distribution summaries, outlier checks, subgroup comparisons, aggregation-risk review, bivariate exploration, categorical profiling, and exploration-readiness scoring.

## Run locally

```bash
bash bash/run_all.sh
```

Optional language examples run only when the matching toolchain is installed.

## Core idea

Descriptive analytics makes observed data legible before stronger claims are made.

```text
raw records → profiling → summaries + distributions
        → visual / subgroup / missingness / anomaly checks
        → questions for inference, forecasting, causal analysis, or modeling
```

A mature exploration workflow does not ask only for averages. It asks what averages hide, which values are missing, where distributions are skewed, whether subgroups behave differently, and what later analytical claims the data can responsibly support.
