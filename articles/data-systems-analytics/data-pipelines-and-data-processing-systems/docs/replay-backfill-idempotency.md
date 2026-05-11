# Replay, backfill, and idempotency notes

A resilient pipeline should be able to revisit history.

Review:

- durable raw inputs
- immutable event logs
- source batch identifiers
- code version
- transformation version
- stable business keys
- merge logic
- deduplication rules
- checkpointing
- replay range
- backfill materiality
- output comparison after rerun

Idempotency means rerunning the same logical input should not create duplicate or contradictory downstream state.
