export type VisualizationContext =
  | "executive_reporting"
  | "technical_validation"
  | "policy_analysis"
  | "operational_monitoring"
  | "legacy_reporting"
  | "model_evaluation";

export type VisualStatus = "approved" | "in_review" | "needs_revision";
export type ChartFit = "high" | "medium" | "low";

export interface VisualizationRegistryItem {
  visualId: string;
  visualTitle: string;
  visualizationContext: VisualizationContext;
  audience: string;
  primaryTask: string;
  owner: string;
  steward: string;
  status: VisualStatus;
  version: string;
  publicationSurface: "report" | "dashboard" | "policy_memo" | "technical_report";
}

export interface ChartAssessment {
  chartId: string;
  visualId: string;
  chartType: string;
  analyticalTask: string;
  chartFit: ChartFit;
  comparisonSupported: boolean;
  exactValuesNeeded: boolean;
  distributionVisible: boolean;
  trendVisible: boolean;
  relationshipVisible: boolean;
}

export interface EncodingAssessment {
  encodingId: string;
  visualId: string;
  primaryEncoding: string;
  axisBaselineAppropriate: boolean;
  sortingAppropriate: boolean;
  colorDependency: boolean;
  perceptualAccuracy: "high" | "medium" | "low";
}

export interface UncertaintyElement {
  uncertaintyId: string;
  visualId: string;
  uncertaintyType: string;
  visualForm: string;
  nearClaim: boolean;
  materiality: "low" | "medium" | "high";
}

export function chartRequiresReview(chart: ChartAssessment): boolean {
  return chart.chartFit !== "high";
}

export function encodingRequiresAccessibilityReview(encoding: EncodingAssessment): boolean {
  return encoding.colorDependency || encoding.perceptualAccuracy === "low";
}

export function uncertaintyPlacementIsWeak(element: UncertaintyElement): boolean {
  return element.materiality === "high" && !element.nearClaim;
}
