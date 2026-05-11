export type TaskType = "binary_classification" | "multiclass_classification" | "regression" | "ranking";
export type PredictionTarget = "class_label" | "event_probability" | "conditional_mean" | "rank_score";
export type ModelStatus = "approved" | "in_review" | "watch" | "planned" | "needs_revision";
export type RiskLevel = "low" | "medium" | "high";

export interface PredictiveModelRegistryItem {
  modelId: string;
  modelName: string;
  taskType: TaskType;
  modelFamily: string;
  predictionTarget: PredictionTarget;
  owner: string;
  steward: string;
  status: ModelStatus;
  riskLevel: RiskLevel;
  intendedUse: string;
}

export interface SplitDesign {
  modelId: string;
  splitStrategy: string;
  trainCount: number;
  validationCount: number;
  testCount: number;
  stratified: boolean;
  timeOrdered: boolean;
  groupAware: boolean;
  testSetProtected: boolean;
  status: ModelStatus;
}

export interface ThresholdPolicy {
  policyId: string;
  modelId: string;
  threshold: number;
  falsePositiveCost: number;
  falseNegativeCost: number;
  reviewStatus: ModelStatus;
}

export interface MonitoringWindow {
  modelId: string;
  windowStart: string;
  windowEnd: string;
  productionMetric: string;
  metricValue: number;
  validationReference: number;
  driftIndex: number;
  status: "approved" | "watch" | "escalate";
}

export function modelRequiresProbabilityCalibration(model: PredictiveModelRegistryItem): boolean {
  return model.predictionTarget === "event_probability";
}

export function splitRequiresReview(split: SplitDesign): boolean {
  return !split.testSetProtected || split.status !== "approved";
}

export function thresholdRequiresGovernance(policy: ThresholdPolicy): boolean {
  return policy.falsePositiveCost !== policy.falseNegativeCost || policy.reviewStatus !== "approved";
}

export function monitoringRequiresEscalation(window: MonitoringWindow): boolean {
  return window.status === "escalate" || window.driftIndex >= 0.18;
}
