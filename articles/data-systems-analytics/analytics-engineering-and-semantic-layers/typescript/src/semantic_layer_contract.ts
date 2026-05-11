export type CertificationStatus = "certified" | "reviewed" | "uncertified";
export type ModelLayer = "staging" | "intermediate" | "mart" | "presentation";
export type LifecycleStatus = "active" | "beta" | "deprecated" | "retired";

export interface AnalyticsModel {
  modelId: string;
  modelName: string;
  layer: ModelLayer;
  domain: string;
  grain: string;
  owner: string;
  lifecycleStatus: LifecycleStatus;
}

export interface SemanticMetric {
  metricId: string;
  metricName: string;
  domain: string;
  definition: string;
  baseModel: string;
  grain: string;
  owner: string;
  certificationStatus: CertificationStatus;
  version: string;
  decisionCritical: boolean;
}

export function metricRequiresGovernanceReview(metric: SemanticMetric): boolean {
  return (
    metric.certificationStatus !== "certified" ||
    metric.grain === "mixed" ||
    metric.decisionCritical
  );
}
