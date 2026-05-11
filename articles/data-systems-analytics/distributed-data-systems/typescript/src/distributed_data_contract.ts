export type NodeStatus = "healthy" | "degraded" | "failed";
export type ReplicaState = "in_sync" | "lagging" | "degraded";
export type ConsistencyModel =
  | "linearizable"
  | "serializable"
  | "snapshot"
  | "causal"
  | "read_committed_or_stale"
  | "eventual";

export interface ClusterNode {
  nodeId: string;
  region: string;
  zone: string;
  role: "leader" | "follower" | "observer";
  status: NodeStatus;
  storageGb: number;
  cpuUtilization: number;
  networkRttMs: number;
  lastHeartbeat: string;
}

export interface ShardMapEntry {
  shardId: string;
  keyRangeStart: number;
  keyRangeEnd: number;
  leaderNode: string;
  replicaNodes: string[];
  replicationFactor: number;
  partitionStrategy: string;
  status: NodeStatus;
}

export interface QuorumPolicy {
  policyId: string;
  workload: string;
  replicationFactor: number;
  readQuorum: number;
  writeQuorum: number;
  consistencyModel: ConsistencyModel;
  availabilityOrientation: "CP" | "AP" | "AP_tolerant" | "mixed";
  status: "approved" | "in_review" | "needs_revision";
}

export function readWriteQuorumsIntersect(policy: QuorumPolicy): boolean {
  return policy.readQuorum + policy.writeQuorum > policy.replicationFactor;
}

export function toleratedMajorityFailures(replicationFactor: number): number {
  return Math.floor((replicationFactor - 1) / 2);
}

export function nodeRequiresReview(node: ClusterNode): boolean {
  return node.status !== "healthy" || node.cpuUtilization > 0.8 || node.networkRttMs > 100;
}
