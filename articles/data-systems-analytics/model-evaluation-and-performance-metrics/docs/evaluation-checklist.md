# Model evaluation checklist

- [ ] The prediction task is explicit.
- [ ] The prediction target is explicit: label, probability, mean, median, quantile, rank, or score.
- [ ] The metric family matches the task.
- [ ] Baseline or naive model comparison is included.
- [ ] Threshold policy is documented for classification decisions.
- [ ] Precision, recall, false positives, and false negatives are reviewed where relevant.
- [ ] ROC-AUC and PR metrics are interpreted as ranking summaries, not deployment decisions.
- [ ] Calibration is assessed when probabilities drive action.
- [ ] Regression errors include average and tail behavior.
- [ ] Subgroup, cohort, and temporal performance are reviewed.
- [ ] Metric uncertainty or validation variability is visible.
- [ ] Monitoring windows and escalation limits are defined before deployment.
