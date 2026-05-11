export type QualityDimension =
  | "accuracy"
  | "completeness"
  | "consistency"
  | "timeliness"
  | "validity"
  | "uniqueness"
  | "interpretability"
  | "accessibility";

export type Severity = "low" | "medium" | "high" | "critical";
export type RuleStatus = "approved" | "in_review" | "needs_revision";

export interface QualityRule {
  ruleId: string;
  dimension: QualityDimension;
  ruleName: string;
  fieldName: string;
  ruleType: string;
  threshold: number;
  severity: Severity;
  owner: string;
  status: RuleStatus;
}

export interface QualityIncident {
  incidentId: string;
  dataset: string;
  ruleId: string;
  failedRecords: number;
  affectedMetric: string;
  incidentStatus: "open" | "in_review" | "closed";
  stewardNotes: string;
}

export interface CleanedRecord {
  canonicalCustomerId: string;
  sourceSystem: string;
  email: string;
  duplicateEmailFlag: boolean;
  qualityIssueCount: number;
}

export function ruleRequiresReview(rule: QualityRule): boolean {
  return rule.status !== "approved" || rule.severity === "critical";
}

export function incidentRequiresEscalation(incident: QualityIncident): boolean {
  return incident.incidentStatus !== "closed" && incident.failedRecords > 0;
}

export function recordRequiresStewardship(record: CleanedRecord): boolean {
  return record.duplicateEmailFlag || record.qualityIssueCount > 0;
}
