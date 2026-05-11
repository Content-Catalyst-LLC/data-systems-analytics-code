# Latency, correctness, and cost tradeoffs

Streaming systems rarely optimize only for speed.

Review:

- how soon partial results should be emitted
- whether late events revise prior outputs
- whether users see provisional labels
- how much state the system must retain
- whether replay can reconstruct serving views
- whether downstream sinks are idempotent
- how much lateness is tolerable by use case
- what cost is acceptable for lower latency
