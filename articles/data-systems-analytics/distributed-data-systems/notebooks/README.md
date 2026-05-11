# Notebook guidance

Use notebooks to inspect distributed-system evidence, not to hide official coordination logic.

Recommended pattern:

1. Run `python/distributed_data_scorecard.py`.
2. Load `outputs/distributed_data_manifest_python.json`.
3. Inspect shard routing, quorum policy, replica lag, operation health, conflicts, consensus events, failover drills, and node health.
4. Compare CP, AP, and mixed workload assumptions.
5. Preserve unresolved consistency and availability risks before relying on distributed outputs.
