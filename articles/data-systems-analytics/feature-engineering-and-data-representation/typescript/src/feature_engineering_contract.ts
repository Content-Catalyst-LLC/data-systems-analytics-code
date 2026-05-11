export type FeatureFamily =
  | "numerical"
  | "numerical_binned"
  | "categorical"
  | "categorical_cross"
  | "temporal"
  | "embedding"
  | "leakage_candidate";

export type FeatureStatus = "approved" | "in_review" | "planned" | "needs_revision";
export type LeakageRisk = "low" | "medium" | "high";

export interface FeatureRegistryItem {
  featureId: string;
  featureName: string;
  featureFamily: FeatureFamily;
  sourceField: string;
  transformation: string;
  modelStage: "training" | "validation" | "deployment";
  status: FeatureStatus;
  owner: string;
  leakageRisk: LeakageRisk;
  interpretability: "high" | "medium" | "low";
  cardinality: string;
}

export interface TransformationRule {
  ruleId: string;
  featureId: string;
  ruleType: string;
  fitScope: "training_only" | "no_fit" | "full_dataset";
  appliedScope: "train_valid_test" | "training_only";
  requiresTrainingFit: boolean;
  allowedAtPredictionTime: boolean;
  reviewStatus: FeatureStatus;
}

export function featureRequiresLeakageReview(feature: FeatureRegistryItem): boolean {
  return feature.leakageRisk !== "low" || feature.status === "needs_revision";
}

export function transformationViolatesEvaluationIntegrity(rule: TransformationRule): boolean {
  return rule.fitScope === "full_dataset" || !rule.allowedAtPredictionTime;
}
