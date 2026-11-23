import type { Product } from "./types";

export type Tone = "drop" | "rise" | "warn" | "neutral";

export interface Status {
  label: string;
  tone: Tone;
}

/** The status chip of a product in the table. */
export function productStatus(product: Product): Status {
  if (product.last_error) return { label: "Check failed", tone: "warn" };
  if (product.last_price === null) return { label: "Waiting", tone: "warn" };
  if (product.target_price !== null && product.last_price <= product.target_price) {
    return { label: "Under target", tone: "drop" };
  }
  const change = product.change_7d ?? 0;
  if (change < -2) return { label: `Down ${Math.round(-change)}%`, tone: "drop" };
  if (change > 2) return { label: `Up ${Math.round(change)}%`, tone: "rise" };
  return { label: "Stable", tone: "neutral" };
}
