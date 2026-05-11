export type ProcessingMode = "batch" | "stream" | "micro_batch" | "replay" | "backfill";
export type StageType = "ingestion" | "validation" | "transformation" | "stateful_processing" | "serving";
export type StageStatus = "approved" | "in_review" | "needs_revision";
export type RunStatus = "success" | "success_with_warning" | "degraded" | "failed";

export interface PipelineStage {
  stageId: string;
  pipelineName: string;
  stageName: string;
  stageType: StageType;
  mode: ProcessingMode;
  upstreamStage?: string;
  downstreamStage?: string;
  owner: string;
  criticality: "low" | "medium" | "high" | "critical";
  status: StageStatus;
}

export interface PipelineRun {
  runId: string;
  pipelineName: string;
  runMode: ProcessingMode;
  inputRows: number;
  outputRows: number;
  failedRows: number;
  retryCount: number;
  status: RunStatus;
  codeVersion: string;
}

export interface QualityGate {
  gateId: string;
  pipelineName: string;
  stageName: string;
  dimension: string;
  ruleName: string;
  threshold: number;
  observedValue: number;
  severity: "low" | "medium" | "high" | "critical";
  status: "pass" | "warn" | "fail";
}

export function stageRequiresReview(stage: PipelineStage): boolean {
  return stage.status !== "approved" || stage.criticality === "critical";
}

export function runFailureRate(run: PipelineRun): number {
  return run.inputRows === 0 ? 0 : run.failedRows / run.inputRows;
}

export function qualityGatePassed(gate: QualityGate): boolean {
  return gate.status === "pass" && gate.observedValue >= gate.threshold;
}
