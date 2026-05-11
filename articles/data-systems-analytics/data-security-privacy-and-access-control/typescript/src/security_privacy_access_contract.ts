export type Classification = "public" | "internal" | "confidential" | "restricted" | "secret";
export type AccessDecision = "allow" | "deny";
export type AccessType = "read" | "read_masked" | "write" | "admin";

export interface DataAsset {
  assetId: string;
  assetName: string;
  domain: string;
  classification: Classification;
  containsPersonalData: boolean;
  containsDirectIdentifiers: boolean;
  sensitivityScore: number;
  owner: string;
  retentionDays: number;
}

export interface AccessPolicy {
  policyId: string;
  assetId: string;
  principalType: string;
  principal: string;
  accessType: AccessType;
  decision: AccessDecision;
  condition: string;
  justification: string;
  reviewFrequencyDays: number;
}

export interface AccessRequest {
  principal: string;
  asset: DataAsset;
  accessType: AccessType;
  purpose: string;
  mfaSatisfied: boolean;
}

export function shouldRequireEnhancedReview(asset: DataAsset): boolean {
  return (
    asset.classification === "restricted" ||
    asset.classification === "secret" ||
    asset.containsDirectIdentifiers ||
    asset.sensitivityScore >= 0.85
  );
}
