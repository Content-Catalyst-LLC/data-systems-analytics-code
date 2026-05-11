# Transactional trust

Transaction evidence should preserve:

- transaction identifier
- start and commit or rollback time
- tables touched
- operation count
- isolation level
- result
- retry count
- rollback status
- latency
- incident linkage when integrity checks fail

A transaction is not only a programming construct. It is a boundary around institutional state change.
