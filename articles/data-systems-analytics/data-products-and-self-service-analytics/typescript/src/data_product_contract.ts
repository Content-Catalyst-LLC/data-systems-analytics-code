export type CertificationStatus = "certified" | "reviewed" | "uncertified";
export type LifecycleStatus = "draft" | "beta" | "active" | "deprecated" | "retired";
export type Criticality = "low" | "medium" | "high";

export interface DataProduct {
  productId: string;
  domain: string;
  productName: string;
  owner: string;
  consumerGroup: string;
  criticality: Criticality;
  freshnessSlaHours: number;
  semanticStatus: CertificationStatus;
  qualityScore: number;
  accessModel: string;
  lifecycleStatus: LifecycleStatus;
}

export interface SemanticMetric {
  metricId: string;
  productId: string;
  metricName: string;
  definition: string;
  grain: string;
  calculationOwner: string;
  certificationStatus: CertificationStatus;
}

export function isDecisionReady(product: DataProduct): boolean {
  return (
    product.lifecycleStatus === "active" &&
    product.semanticStatus === "certified" &&
    product.qualityScore >= 0.9
  );
}
