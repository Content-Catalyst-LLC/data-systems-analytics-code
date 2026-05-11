export type ArchitectureZone =
  | "raw_lake"
  | "bronze_lakehouse"
  | "silver_lakehouse"
  | "gold_lakehouse"
  | "warehouse_dimension"
  | "warehouse_fact"
  | "feature_store"
  | "sandbox_lake"
  | "archive_lake";

export type SchemaStrategy = "schema_on_read" | "schema_on_write" | "hybrid_schema";
export type GovernanceStatus = "certified" | "registered" | "in_review" | "unregistered";

export interface DataAsset {
  assetId: string;
  assetName: string;
  architectureZone: ArchitectureZone;
  storageForm: "object_storage" | "relational_table" | "table";
  schemaStrategy: SchemaStrategy;
  fileOrTableFormat: string;
  owner: string;
  governanceStatus: GovernanceStatus;
  rowCount: number;
  sizeGb: number;
  freshnessHours: number;
  piiClassification: "public" | "internal" | "confidential" | "restricted";
  queryFrequencyPerDay: number;
  mlReady: boolean;
}

export interface LakehouseFeatureSet {
  assetId: string;
  openTableFormat: "delta" | "iceberg" | "hudi" | "parquet_only";
  acidTransactions: boolean;
  schemaEvolution: boolean;
  timeTravel: boolean;
  partitionEvolution: boolean;
  batchStreamUnified: boolean;
  metadataScalability: boolean;
}

export function assetNeedsGovernanceReview(asset: DataAsset): boolean {
  return asset.governanceStatus !== "certified" && asset.piiClassification !== "public";
}

export function isWarehouseAsset(asset: DataAsset): boolean {
  return asset.architectureZone === "warehouse_dimension" || asset.architectureZone === "warehouse_fact";
}

export function isLakehouseManaged(features: LakehouseFeatureSet): boolean {
  return features.acidTransactions && features.schemaEvolution && features.timeTravel && features.metadataScalability;
}
