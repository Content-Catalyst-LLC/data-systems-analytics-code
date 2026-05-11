# Pipeline design checklist

- [ ] Pipeline stages are represented as an explicit graph.
- [ ] Processing mode is documented: batch, stream, micro-batch, replay, or backfill.
- [ ] Stage owners and criticality levels are assigned.
- [ ] Quality gates run before downstream promotion.
- [ ] Orchestration dependencies are explicit.
- [ ] Idempotent rerun behavior is tested.
- [ ] Replay and backfill procedures are documented.
- [ ] Lineage edges connect sources, stages, and outputs.
- [ ] Observability covers throughput, latency, lag, errors, freshness, and backpressure.
- [ ] Delivery semantics are documented end to end.
