export type InteroperabilityLayer =
  | "technical"
  | "syntactic"
  | "semantic"
  | "organizational"
  | "identity"
  | "observability"
  | "security"
  | "lifecycle";

export type SemanticRisk = "low" | "medium" | "high";
export type MappingStatus = "active" | "review" | "deprecated";

export interface SourceSystem {
  systemId: string;
  systemName: string;
  domain: string;
  owner: string;
  primaryEntity: string;
  identifierField: string;
  sensitivity: "low" | "medium" | "high";
}

export interface SchemaMapping {
  mappingId: string;
  sourceSystem: string;
  targetModel: string;
  sourceField: string;
  targetField: string;
  transformationType: string;
  semanticRisk: SemanticRisk;
  owner: string;
  status: MappingStatus;
}

export interface InteroperabilityCheck {
  checkId: string;
  layer: InteroperabilityLayer;
  expectedValue: number;
  observedValue: number;
  status: "pass" | "warn" | "fail";
  owner: string;
}

export function mappingNeedsReview(mapping: SchemaMapping): boolean {
  return mapping.semanticRisk === "high" || mapping.status === "review";
}
