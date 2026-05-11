export type CertificationStatus = "certified" | "reviewed" | "uncertified";
export type LifecycleStatus = "active" | "beta" | "deprecated" | "retired";

export interface BIMetric {
  metricId: string;
  metricName: string;
  domain: string;
  owner: string;
  semanticStatus: CertificationStatus;
  qualityScore: number;
  freshnessHours: number;
  uncertaintyVisible: boolean;
  decisionCritical: boolean;
}

export interface Dashboard {
  dashboardId: string;
  dashboardName: string;
  domain: string;
  primaryUser: string;
  decisionFunction:
    | "descriptive-monitoring"
    | "diagnostic-analysis"
    | "threshold-monitoring"
    | "trend-review"
    | "scenario-evaluation";
  certificationStatus: CertificationStatus;
  refreshSlaHours: number;
  owner: string;
  lifecycleStatus: LifecycleStatus;
}

export function isDecisionReadyDashboard(dashboard: Dashboard): boolean {
  return (
    dashboard.lifecycleStatus === "active" &&
    dashboard.certificationStatus === "certified" &&
    dashboard.refreshSlaHours <= 24
  );
}
