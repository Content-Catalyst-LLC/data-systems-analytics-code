export type WindowType = "tumbling" | "sliding" | "session";
export type OutputMode = "append" | "update" | "append_then_update";
export type DeliverySemantics = "at_most_once" | "at_least_once" | "exactly_once_effective";
export type ReviewStatus = "approved" | "in_review" | "needs_revision";

export interface EventRecord {
  eventId: string;
  eventKey: string;
  eventType: string;
  eventTime: string;
  processingTime: string;
  region: string;
  sourceSystem: string;
  value: number;
  quantity: number;
  qualityScore: number;
}

export interface WindowDefinition {
  windowId: string;
  windowType: WindowType;
  sizeSeconds: number;
  slideSeconds: number;
  allowedLatenessSeconds: number;
  triggerPolicy: string;
  outputMode: OutputMode;
  status: ReviewStatus;
}

export interface StreamTopic {
  topicId: string;
  topicName: string;
  eventDomain: string;
  retentionHours: number;
  partitionCount: number;
  replicationFactor: number;
  deliverySemantics: DeliverySemantics;
  status: ReviewStatus;
}

export function latenessSeconds(event: EventRecord): number {
  return Math.max(0, (Date.parse(event.processingTime) - Date.parse(event.eventTime)) / 1000);
}

export function windowRequiresReview(window: WindowDefinition): boolean {
  return window.status !== "approved" || window.allowedLatenessSeconds === 0;
}

export function topicSupportsReplay(topic: StreamTopic, requiredHours: number): boolean {
  return topic.retentionHours >= requiredHours;
}
