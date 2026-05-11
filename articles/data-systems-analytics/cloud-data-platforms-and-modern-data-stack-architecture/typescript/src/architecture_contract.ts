export type StackLayer =
  | "source"
  | "ingestion"
  | "storage"
  | "transformation"
  | "orchestration"
  | "metadata"
  | "lineage"
  | "semantic"
  | "serving"
  | "consumption"
  | "ai_ml";

export interface StackComponent {
  componentId: string;
  layer: StackLayer;
  owner: string;
  criticality: "low" | "medium" | "high";
  governanceControl: string;
  observabilityControl: string;
}

export interface PipelineContract {
  pipelineId: string;
  sourceLayer: StackLayer;
  targetLayer: StackLayer;
  latencyPattern: "batch" | "micro-batch" | "cdc" | "event" | "stream";
  owner: string;
  qualityGate: string;
}

export const requiredLayers: StackLayer[] = [
  "source",
  "ingestion",
  "storage",
  "transformation",
  "orchestration",
  "metadata",
  "lineage",
  "semantic",
  "serving",
  "consumption"
];

export function missingLayers(components: StackComponent[]): StackLayer[] {
  const present = new Set(components.map((component) => component.layer));
  return requiredLayers.filter((layer) => !present.has(layer));
}
