export type MappingStatus = "approved" | "in_review" | "needs_revision";
export type TestStatus = "pass" | "warn" | "fail";
export type PipelineStatus = "completed" | "completed_with_warning" | "failed";

export interface StatusMapping {
  sourceSystem: string;
  sourceField: string;
  sourceValue: string;
  canonicalDomain: string;
  canonicalValue: string;
  activeFlag: boolean;
  mappingStatus: MappingStatus;
}

export interface TransformationTest {
  testId: string;
  testName: string;
  scope: "customer" | "order" | "mapping" | "load" | "governance";
  condition: string;
  expectedResult: "pass";
  severity: "low" | "medium" | "high" | "critical";
  status: TestStatus;
}

export interface OrchestrationRun {
  runId: string;
  pipelineName: string;
  sourceBatchId: string;
  codeVersion: string;
  inputRows: number;
  loadedRows: number;
  rejectedRows: number;
  status: PipelineStatus;
}

export function mappingRequiresReview(mapping: StatusMapping): boolean {
  return mapping.mappingStatus !== "approved";
}

export function testRequiresRemediation(test: TransformationTest): boolean {
  return test.status !== "pass";
}

export function rejectRate(run: OrchestrationRun): number {
  return run.inputRows === 0 ? 0 : run.rejectedRows / run.inputRows;
}
