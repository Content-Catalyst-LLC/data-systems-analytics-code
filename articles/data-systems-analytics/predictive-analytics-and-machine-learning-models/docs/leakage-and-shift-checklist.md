# Leakage and distribution-shift checklist

- [ ] No future information enters training or validation.
- [ ] No target-derived feature is used improperly.
- [ ] Duplicate or related records do not cross partitions.
- [ ] Preprocessing occurs inside pipelines.
- [ ] Resampling is performed only inside training folds.
- [ ] Temporal validation preserves chronological order.
- [ ] Production data distribution is compared with validation data.
- [ ] Label definitions remain stable.
- [ ] Drift thresholds are documented.
- [ ] Recalibration, retraining, rollback, or retirement path exists.
