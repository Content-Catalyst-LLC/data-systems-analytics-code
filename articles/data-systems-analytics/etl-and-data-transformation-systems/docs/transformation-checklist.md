# ETL and transformation checklist

- [ ] Raw extracts are preserved.
- [ ] Staging tables are inspectable.
- [ ] Canonical targets define grain, identity, and meaning.
- [ ] Status, code, unit, and timestamp mappings are governed.
- [ ] Data-quality checks run before promotion.
- [ ] Rejected records are quarantined with reason codes.
- [ ] Incremental merges are idempotent.
- [ ] CDC operations are ordered by sequence or commit time.
- [ ] Lineage links outputs to sources, mappings, code version, and run ID.
- [ ] Backfill and replay procedures are documented.
