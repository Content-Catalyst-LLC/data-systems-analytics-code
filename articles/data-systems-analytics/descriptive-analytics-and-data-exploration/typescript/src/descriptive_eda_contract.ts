export type VariableType = "identifier" | "categorical" | "period" | "numeric" | "binary";
export type CheckStatus = "pass" | "in_review" | "warn" | "fail";
export type Severity = "low" | "medium" | "high" | "critical";

export interface VariableProfile {
  variableName: string;
  variableType: VariableType;
  expectedDomain: string;
  nullable: boolean;
  description: string;
}

export interface ExplorationCheck {
  checkId: string;
  checkType: string;
  status: CheckStatus;
  severity: Severity;
  evidence: string;
  remediation: string;
}

export interface NumericProfile {
  variableName: string;
  n: number;
  nonMissing: number;
  missing: number;
  missingRate: number;
  mean: number;
  median: number;
  min: number;
  max: number;
  outlierCountIqr: number;
}

export function checkRequiresReview(check: ExplorationCheck): boolean {
  return check.status !== "pass";
}

export function variableAllowsMissing(profile: VariableProfile): boolean {
  return profile.nullable;
}

export function profileSuggestsSkew(profile: NumericProfile): boolean {
  return Math.abs(profile.mean - profile.median) > 0.1 * Math.max(Math.abs(profile.median), 1);
}
