export type TaskType = "binary_classification" | "multiclass_classification" | "regression" | "ranking";
export type PredictionTarget = "class_label" | "event_probability" | "conditional_mean" | "conditional_median" | "quantile" | "rank";
export type ModelStatus = "approved" | "in_review" | "watch" | "needs_revision";
export type RiskLevel = "low" | "medium" | "high";

export interface ModelRegistryItem {
  modelId: string;
  modelName: string;
  taskType: TaskType;
  predictionTarget: PredictionTarget;
  owner: string;
  steward: string;
  status: ModelStatus;
  version: string;
  intendedUse: string;
  riskLevel: RiskLevel;
}

export interface ThresholdPolicy {
  policyId: string;
  modelId: string;
  threshold: number;
  policyName: string;
  falsePositiveCost: number;
  falseNegativeCost: number;
  decisionOwner: string;
  reviewStatus: ModelStatus;
}

export interface MetricScorecardItem {
  metricId: string;
  modelId: string;
  metricName: string;
  metricFamily: "ranking" | "threshold" | "calibration" | "regression" | "monitoring";
  targetQuestion: string;
  acceptableLimit: number;
  observedValue: number;
  status: ModelStatus;
}

export function thresholdNeedsGovernance(policy: ThresholdPolicy): boolean {
  return policy.falseNegativeCost !== policy.falsePositiveCost || policy.reviewStatus !== "approved";
}

export function metricNeedsReview(metric: MetricScorecardItem): boolean {
  return metric.status !== "approved";
}

export function probabilityTargetRequiresCalibration(model: ModelRegistryItem): boolean {
  return model.predictionTarget === "event_probability";
}
