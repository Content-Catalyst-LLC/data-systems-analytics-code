# Streaming analytics checklist

- [ ] Event schema is documented.
- [ ] Event-time field is authoritative and populated.
- [ ] Processing time is recorded.
- [ ] Window type, size, and allowed lateness are explicit.
- [ ] Watermark behavior is monitored.
- [ ] Late data policy is documented.
- [ ] Trigger policy is documented.
- [ ] Output mode is labeled as provisional, update, append, or final.
- [ ] Stateful aggregates are checkpointed or recoverable.
- [ ] Event log retention supports replay.
- [ ] Delivery semantics are stated end to end.
- [ ] Alert rules are reviewed for severity, threshold, and owner.
