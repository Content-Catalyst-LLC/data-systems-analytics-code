export type ForecastModelFamily =
  | "seasonal_naive"
  | "moving_average"
  | "time_series_regression"
  | "sarima"
  | "linear_trend";

export type ValidationDesign = "rolling_origin" | "static_holdout";
export type ForecastStatus = "approved" | "in_review" | "planned" | "needs_revision";

export interface ForecastModel {
  modelId: string;
  seriesId: string;
  modelName: string;
  modelFamily: ForecastModelFamily;
  frequency: "daily" | "weekly" | "monthly" | "quarterly" | "annual";
  horizon: number;
  usesExogenous: boolean;
  validationDesign: ValidationDesign;
  status: ForecastStatus;
  owner: string;
}

export interface ForecastRecord {
  forecastId: string;
  modelId: string;
  seriesId: string;
  originDate: string;
  horizon: number;
  forecast: number;
  lower80: number;
  upper80: number;
  lower95: number;
  upper95: number;
  releaseStatus: ForecastStatus;
}

export function modelRequiresReview(model: ForecastModel): boolean {
  return model.validationDesign !== "rolling_origin" || model.status !== "approved";
}

export function intervalWidth80(record: ForecastRecord): number {
  return record.upper80 - record.lower80;
}

export function intervalWidth95(record: ForecastRecord): number {
  return record.upper95 - record.lower95;
}
