export type DashboardType =
  | "monitoring"
  | "exploratory"
  | "guided_story"
  | "operational_monitoring"
  | "legacy_reporting";

export type DashboardStatus = "approved" | "in_review" | "needs_revision";
export type FilterType = "dropdown" | "multiselect" | "range_slider" | "search" | "parameter";
export type VisualType = "kpi_cards" | "line_chart" | "bar_chart" | "table" | "matrix" | "annotation_panel" | "kpi_grid";

export interface DashboardRegistryItem {
  dashboardId: string;
  dashboardTitle: string;
  dashboardType: DashboardType;
  audience: string;
  primaryUse: string;
  owner: string;
  steward: string;
  status: DashboardStatus;
  refreshCadence: "hourly" | "daily" | "weekly" | "monthly";
  viewCount: number;
  filterCount: number;
}

export interface KpiDefinition {
  kpiId: string;
  dashboardId: string;
  kpiName: string;
  definitionStatus: "approved" | "review" | "incomplete";
  baselinePresent: boolean;
  targetPresent: boolean;
  trendPresent: boolean;
  denominatorPresent: boolean;
}

export interface FilterControl {
  filterId: string;
  dashboardId: string;
  filterName: string;
  filterType: FilterType;
  defaultStateVisible: boolean;
  resetAvailable: boolean;
  consumerRelevant: boolean;
  complexityLevel: "low" | "medium" | "high";
}

export interface StoryPoint {
  storyPointId: string;
  dashboardId: string;
  sequenceOrder: number;
  storyTitle: string;
  storyFunction: "context" | "pattern" | "tradeoff" | "status" | "governance_warning";
  claimId: string;
  linkedViewId: string;
  uncertaintyVisible: boolean;
}

export function hasClutterRisk(dashboard: DashboardRegistryItem): boolean {
  return dashboard.viewCount > 3 || dashboard.filterCount > 5;
}

export function kpiIsNaked(kpi: KpiDefinition): boolean {
  return !kpi.baselinePresent || !kpi.trendPresent || !kpi.denominatorPresent;
}

export function filterAddsFriction(filter: FilterControl): boolean {
  return !filter.defaultStateVisible || !filter.resetAvailable || !filter.consumerRelevant || filter.complexityLevel === "high";
}
