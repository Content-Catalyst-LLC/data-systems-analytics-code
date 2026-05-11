# Relational design checklist

- [ ] Every entity and event table has a defined grain.
- [ ] Primary keys are stable and documented.
- [ ] Foreign keys express governed relationships.
- [ ] Nullability, uniqueness, check constraints, and domains are explicit.
- [ ] Normalization risks are reviewed.
- [ ] Indexes are tied to workload evidence.
- [ ] Query plans and latency are monitored for critical workloads.
- [ ] Transactions have expected isolation levels.
- [ ] Rollbacks, deadlocks, and retries are measured.
- [ ] Access controls follow least privilege.
