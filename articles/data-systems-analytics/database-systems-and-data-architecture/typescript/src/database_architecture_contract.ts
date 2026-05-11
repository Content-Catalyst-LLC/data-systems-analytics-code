export type SystemType =
  | "operational_database"
  | "analytical_database"
  | "analytical_storage"
  | "streaming_platform"
  | "governance_platform"
  | "records_platform"
  | "analytics_service"
  | "ml_data_platform";

export type CertificationStatus = "certified" | "registered" | "in_review" | "missing";
export type ControlStatus = "pass" | "approved" | "good" | "registered" | "in_review" | "watch" | "warn" | "missing";

export interface DatabaseSystem {
  systemId: string;
  systemName: string;
  systemType: SystemType;
  storageModel: string;
  primaryWorkload: string;
  owner: string;
  criticality: "low" | "medium" | "high" | "critical";
  recordsMillions: number;
  dataVolumeGb: number;
  availabilityTarget: number;
  certificationStatus: CertificationStatus;
}

export interface SchemaAsset {
  assetId: string;
  systemId: string;
  assetName: string;
  assetType: string;
  grain: string;
  primaryKey: string;
  foreignKeyCount: number;
  constraintCount: number;
  owner: string;
  classification: "public" | "internal" | "confidential" | "restricted";
  lineageStatus: "complete" | "partial" | "missing";
  qualityStatus: ControlStatus;
  accessStatus: ControlStatus;
  lifecycleStatus: ControlStatus;
}

export interface ArchitectureRisk {
  riskId: string;
  riskArea: string;
  systemId: string;
  description: string;
  severity: "low" | "medium" | "high" | "critical";
  likelihood: "low" | "medium" | "high";
  owner: string;
  status: "resolved" | "in_review" | "planned" | "watch";
}

export function systemRequiresReview(system: DatabaseSystem): boolean {
  return system.certificationStatus !== "certified" || system.criticality === "critical";
}

export function assetRequiresGovernanceReview(asset: SchemaAsset): boolean {
  return asset.lineageStatus !== "complete" || asset.qualityStatus !== "pass" || asset.accessStatus !== "approved";
}

export function isHighRisk(risk: ArchitectureRisk): boolean {
  return risk.severity === "critical" || (risk.severity === "high" && risk.likelihood !== "low");
}
