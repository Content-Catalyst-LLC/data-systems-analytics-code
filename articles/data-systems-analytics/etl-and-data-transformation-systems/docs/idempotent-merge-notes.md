# Idempotent merge notes

Idempotent ETL means a rerun, retry, or replay should not create duplicate or contradictory target state.

Review:

- stable business keys
- deterministic surrogate-key generation
- deduplication rules
- operation ordering
- merge strategy for inserts, updates, and deletes
- late correction handling
- rejected-record behavior
- replay window and source retention
- target table history policy
