export type Classification = "public" | "internal" | "confidential" | "restricted";
export type Criticality = "low" | "medium" | "high";
export type CertificationStatus = "certified" | "reviewed" | "uncertified";
export type LifecycleStatus = "active" | "deprecated" | "retired";

export interface GovernedDataAsset {
  assetId: string;
  assetName: string;
  domain: string;
  assetType: string;
  owner: string;
  steward: string;
  classification: Classification;
  criticality: Criticality;
  certificationStatus: CertificationStatus;
  lifecycleStatus: LifecycleStatus;
}

export interface StewardshipRole {
  roleId: string;
  personOrGroup: string;
  roleType: "data_steward" | "data_owner" | "policy_owner" | "control_owner";
  domain: string;
  responsibilityScope: string;
  decisionAuthority: string;
  active: boolean;
}

export interface AccessReview {
  accessId: string;
  assetId: string;
  requesterGroup: string;
  purpose: string;
  accessLevel: "read" | "write" | "export" | "admin";
  riskLevel: Criticality;
  decision: "approved" | "approved_with_conditions" | "denied";
  expiryDays: number;
}

export function requiresHighControl(asset: GovernedDataAsset): boolean {
  return asset.classification === "restricted" || asset.criticality === "high";
}

export function accessShouldExpire(review: AccessReview): boolean {
  return review.accessLevel === "export" || review.riskLevel === "high" || review.expiryDays <= 90;
}
