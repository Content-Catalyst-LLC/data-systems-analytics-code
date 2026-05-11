# Consistency tradeoffs

Distributed data design is a tradeoff space, not a universal optimization problem.

Review:

- what must be linearizable
- what can tolerate stale reads
- what can be eventually consistent
- which operations must be atomic across shards
- whether conflicts are acceptable
- whether the application can reconcile conflicts
- whether users need monotonic reads or read-your-writes
- whether availability matters more than immediate global agreement
- what happens during network partition
