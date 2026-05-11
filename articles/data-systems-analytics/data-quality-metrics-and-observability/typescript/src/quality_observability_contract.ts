export type QualityDimension =
  | "accuracy"
  | "completeness"
  | "validity"
  | "consistency"
  | "timeliness"
  | "freshness"
  | "uniqueness"
  | "integrity"
  | "volume"
  | "distribution"
  | "schema";

export type CheckStatus = "pass" | "warn" | "fail";
export type Criticality = "low" | "medium" | "high";

export interface DatasetRegistryEntry {
  datasetId: string;
  datasetName: string;
  domain: string;
  owner: string;
  criticality: Criticality;
  expectedFreshnessHours: number;
  certificationStatus: "certified" | "reviewed" | "uncertified";
}

export interface QualityCheck {
  checkId: string;
  datasetId: string;
  qualityDimension: QualityDimension;
  checkName: string;
  expectedValue: number;
  observedValue: number;
  status: CheckStatus;
  severity: Criticality;
  owner: string;
}

export interface QualityIncident {
  incidentId: string;
  datasetId: string;
  severity: Criticality;
  status: "open" | "in_review" | "resolved";
  rootCauseCategory: string;
  consumerNotified: boolean;
}

export function requiresImmediateReview(check: QualityCheck): boolean {
  return check.status === "fail" || (check.status === "warn" && check.severity === "high");
}
