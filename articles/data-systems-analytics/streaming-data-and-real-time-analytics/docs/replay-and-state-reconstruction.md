# Replay and state reconstruction

A durable stream can support reconstructable state when:

- events are immutable
- event schemas are versioned
- topic retention is long enough for replay needs
- consumer offsets or checkpoints are recoverable
- transformation logic is versioned
- downstream materialized views can be rebuilt
- late-event and correction policies are documented

Replay is where real-time analytics connects to reproducible analytics.
