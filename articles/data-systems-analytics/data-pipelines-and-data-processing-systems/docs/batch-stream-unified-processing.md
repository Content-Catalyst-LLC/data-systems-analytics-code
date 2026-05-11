# Batch, streaming, and unified processing notes

Batch is useful for bounded recomputation, historical backfills, and reproducible refreshes.

Streaming is useful for unbounded event flows, low-latency state, and continuous updates.

Unified processing emphasizes that bounded and unbounded data can be represented through common dataflow concepts:

- sources
- collections or streams
- transforms
- windows
- triggers
- state
- sinks
- runners or execution engines

The design question is not batch versus stream as ideology. It is how timing, correctness, cost, state, and governance match the workload.
