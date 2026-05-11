export type ConstraintType =
  | "primary_key"
  | "foreign_key"
  | "unique"
  | "check"
  | "not_null";

export type CertificationStatus = "certified" | "registered" | "in_review" | "missing";
export type IsolationLevel = "read_committed" | "repeatable_read" | "serializable";

export interface RelationTable {
  tableId: string;
  tableName: string;
  entityType: "entity" | "event" | "classification";
  grain: string;
  primaryKey: string;
  owner: string;
  normalizationTarget: string;
  certificationStatus: CertificationStatus;
}

export interface RelationalConstraint {
  constraintId: string;
  tableName: string;
  columnName: string;
  constraintType: ConstraintType;
  referencedTable?: string;
  referencedColumn?: string;
  ruleExpression: string;
  severity: "low" | "medium" | "high" | "critical";
  status: "approved" | "in_review" | "missing";
}

export interface TransactionRecord {
  txnId: string;
  tablesTouched: string[];
  isolationLevel: IsolationLevel;
  result: "committed" | "rolled_back" | "failed";
  rollbackFlag: boolean;
  deadlockRetryCount: number;
  latencyMs: number;
}

export function isRelationshipConstraint(constraint: RelationalConstraint): boolean {
  return constraint.constraintType === "foreign_key";
}

export function tableRequiresReview(table: RelationTable): boolean {
  return table.certificationStatus !== "certified" || table.grain.length === 0 || table.primaryKey.length === 0;
}

export function transactionRequiresReview(txn: TransactionRecord): boolean {
  return txn.result !== "committed" || txn.rollbackFlag || txn.deadlockRetryCount > 0 || txn.latencyMs > 500;
}
