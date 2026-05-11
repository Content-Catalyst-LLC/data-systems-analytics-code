# Feature leakage checklist

- [ ] Feature is available at prediction time.
- [ ] Feature is not calculated using the target.
- [ ] Feature is not calculated using future observations.
- [ ] Aggregations respect cutoff time.
- [ ] Preprocessing is fit only on training data.
- [ ] Validation and test data are transformed, not refit.
- [ ] Cross-validation folds contain complete preprocessing pipelines.
- [ ] Global statistics are not computed on all data before splitting.
- [ ] Deployment source system can produce the feature consistently.
- [ ] Feature owner has approved the availability and meaning.
