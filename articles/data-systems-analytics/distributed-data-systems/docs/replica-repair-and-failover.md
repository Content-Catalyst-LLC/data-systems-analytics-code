# Replica repair and failover notes

Replica health depends on more than node uptime.

Review:

- commit index and applied index
- leader health
- follower lag
- snapshot age
- quorum availability
- zone and region placement
- anti-entropy or repair process
- election timeout behavior
- failover recovery time
- data loss or acknowledged-write loss
