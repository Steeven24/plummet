// The JSON shapes the Plummet API returns (see apps/api/src/plummet_api/schemas.py).

export interface Product {
  id: number;
  url: string;
  store: string;
  name: string | null;
  currency: string;
  target_price: number | null;
  last_price: number | null;
  alerts_enabled: boolean;
  price_selector: string | null;
  last_checked_at: string | null;
  last_error: string | null;
  created_at: string;
  trend: number[];
  change_7d: number | null;
}

export interface PricePoint {
  checked_at: string;
  price: number;
}

export interface Overview {
  products: number;
  stores: number;
  below_target: number;
  alerts_week: number;
  alerts_today: number;
  savings: number;
  currency: string | null;
}

export interface SentAlert {
  id: number;
  product_id: number;
  product_name: string;
  kind: "below_target" | "price_drop";
  text: string;
  delivered: boolean;
  error: string | null;
  created_at: string;
}

export interface CheckRun {
  started_at: string;
  seconds: number;
  checked: number;
  alerts: number;
  errors: number;
}

export interface CronStatus {
  schedule: string;
  interval_minutes: number;
  last_run: CheckRun | null;
  next_run_at: string | null;
  runs_week: number;
  success_rate: number | null;
  avg_seconds: number | null;
}

export interface LogLine {
  date: string;
  time: string;
  level: string;
  message: string;
}
