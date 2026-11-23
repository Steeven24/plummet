import type { CronStatus, LogLine, Overview, PricePoint, Product, SentAlert } from "./types";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!response.ok) {
    // FastAPI sends errors as {"detail": "..."}.
    const body = await response.json().catch(() => null);
    const detail = typeof body?.detail === "string" ? body.detail : response.statusText;
    throw new ApiError(detail || "Request failed", response.status);
  }
  return (response.status === 204 ? undefined : await response.json()) as T;
}

export interface NewProduct {
  url: string;
  target_price?: number | null;
}

export type ProductChanges = Partial<
  Pick<Product, "target_price" | "alerts_enabled" | "price_selector">
>;

export const api = {
  products: () => request<Product[]>("/api/products"),
  history: (id: number, days: number) =>
    request<PricePoint[]>(`/api/products/${id}/history?days=${days}`),
  addProduct: (data: NewProduct) =>
    request<Product>("/api/products", { method: "POST", body: JSON.stringify(data) }),
  updateProduct: (id: number, changes: ProductChanges) =>
    request<Product>(`/api/products/${id}`, { method: "PATCH", body: JSON.stringify(changes) }),
  deleteProduct: (id: number) => request<void>(`/api/products/${id}`, { method: "DELETE" }),
  overview: () => request<Overview>("/api/overview"),
  alerts: () => request<SentAlert[]>("/api/alerts?days=7&limit=10"),
  cron: () => request<CronStatus>("/api/cron"),
  logs: () => request<LogLine[]>("/api/cron/logs?lines=8"),
};
