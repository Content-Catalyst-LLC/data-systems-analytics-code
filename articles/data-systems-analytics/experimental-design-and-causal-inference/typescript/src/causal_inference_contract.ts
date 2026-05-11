export type CausalDesign =
  | "randomized_experiment"
  | "difference_in_differences"
  | "regression_discontinuity"
  | "target_trial_emulation"
  | "observational_regression";

export type Estimand = "ATE" | "ATT" | "LATE" | "CATE" | "ITT" | "TOT";
export type StudyStatus = "approved" | "in_review" | "planned" | "needs_revision";
export type RiskLevel = "low" | "medium" | "high";

export interface CausalStudy {
  studyId: string;
  causalQuestion: string;
  intervention: string;
  comparison: string;
  outcome: string;
  unitOfAnalysis: string;
  designType: CausalDesign;
  estimand: Estimand;
  owner: string;
  status: StudyStatus;
  riskLevel: RiskLevel;
}

export interface AssumptionCheck {
  checkId: string;
  studyId: string;
  assumption: string;
  status: "pass" | "warn" | "fail" | "planned";
  severity: "low" | "medium" | "high" | "critical";
  remediation: string;
}

export function studyRequiresGovernanceReview(study: CausalStudy): boolean {
  return study.status !== "approved" || study.riskLevel === "high";
}

export function assumptionRequiresRemediation(check: AssumptionCheck): boolean {
  return check.status === "warn" || check.status === "fail";
}
