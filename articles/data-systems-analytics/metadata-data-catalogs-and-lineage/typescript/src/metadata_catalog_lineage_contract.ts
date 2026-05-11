export type AssetType =
  | "table"
  | "view"
  | "data_product"
  | "event_stream"
  | "feature_table"
  | "dashboard"
  | "model"
  | "extract";

export type CertificationStatus = "certified" | "reviewed" | "uncertified";
export type MetadataType = "technical" | "business" | "operational" | "administrative" | "policy" | "semantic" | "social_usage";
export type LineageGranularity = "dataset" | "column" | "pipeline" | "analytical" | "semantic" | "unknown";

export interface DataAsset {
  assetId: string;
  assetName: string;
  domain: string;
  assetType: AssetType;
  owner: string;
  steward: string;
  classification: "public" | "internal" | "confidential" | "restricted";
  certificationStatus: CertificationStatus;
  criticality: "low" | "medium" | "high";
}

export interface MetadataElement {
  metadataId: string;
  assetId: string;
  metadataType: MetadataType;
  elementName: string;
  valuePresent: boolean;
  qualityStatus: "approved" | "review" | "stale" | "missing";
}

export interface LineageEdge {
  edgeId: string;
  upstreamAsset: string;
  downstreamAsset: string;
  relationshipType: string;
  lineageGranularity: LineageGranularity;
  impactLevel: "low" | "medium" | "high";
}

export interface ProvenanceEvent {
  eventId: string;
  assetId: string;
  provEntity: string;
  provActivity: string;
  provAgent: string;
  versionId: string;
  provenanceComplete: boolean;
}

export function requiresMetadataReview(element: MetadataElement): boolean {
  return !element.valuePresent || element.qualityStatus === "missing" || element.qualityStatus === "stale";
}
