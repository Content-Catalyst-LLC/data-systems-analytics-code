export type ModelFamily =
  | "two_sample_estimator"
  | "linear_regression"
  | "multiple_regression"
  | "null_hypothesis_test";

export type StudyStatus = "approved" | "in_review" | "needs_revision";
export type RiskLevel = "low" | "medium" | "high";

export interface StatisticalModelRecord {
  modelId: string;
  modelName: string;
  modelFamily: ModelFamily;
  estimand: string;
  outcome: string;
  predictors: string[];
  assumptionProfile: string;
  status: StudyStatus;
  owner: string;
  riskLevel: RiskLevel;
}

export interface InferenceClaim {
  claimId: string;
  modelId: string;
  claimType: string;
  effectSize: number;
  standardError: number;
  pValue: number;
  confidenceLow: number;
  confidenceHigh: number;
  practicalThreshold: number;
  claimStatus: StudyStatus;
}

export function claimNeedsPracticalReview(claim: InferenceClaim): boolean {
  return Math.abs(claim.effectSize) < Math.abs(claim.practicalThreshold);
}

export function intervalCrossesZero(claim: InferenceClaim): boolean {
  return claim.confidenceLow <= 0 && claim.confidenceHigh >= 0;
}

export function modelNeedsAssumptionReview(model: StatisticalModelRecord): boolean {
  return model.assumptionProfile === "unclear_assumptions" || model.status !== "approved";
}
