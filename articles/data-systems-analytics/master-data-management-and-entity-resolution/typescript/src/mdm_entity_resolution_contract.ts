export type EntityType =
  | "organization"
  | "person"
  | "facility"
  | "product"
  | "asset"
  | "household"
  | "legal_entity";

export type MatchAction =
  | "merge"
  | "link"
  | "possible_link"
  | "steward_review"
  | "block";

export type LinkStatus = "active" | "review" | "retired";

export interface SourceRecord {
  recordId: string;
  sourceSystem: string;
  domain: string;
  entityType: EntityType;
  sourceEntityId: string;
  name: string;
  legalIdentifier?: string;
  recordStatus: "active" | "inactive";
}

export interface CandidateMatch {
  candidateId: string;
  leftRecordId: string;
  rightRecordId: string;
  entityType: EntityType;
  matchMethod: string;
  matchScore: number;
  recommendedAction: MatchAction;
  reviewRequired: boolean;
}

export interface MasterEntity {
  masterEntityId: string;
  entityType: EntityType;
  masterName: string;
  domain: string;
  authoritativeView: string;
  lifecycleStatus: "active" | "inactive" | "retired";
  steward: string;
}

export function requiresStewardReview(candidate: CandidateMatch): boolean {
  return (
    candidate.reviewRequired ||
    candidate.recommendedAction === "steward_review" ||
    candidate.recommendedAction === "possible_link" ||
    (candidate.recommendedAction === "merge" && candidate.matchScore < 0.95)
  );
}
