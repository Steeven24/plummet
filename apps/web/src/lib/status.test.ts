import { describe, expect, it } from "vitest";

import { productStatus } from "./status";
import type { Product } from "./types";

function product(changes: Partial<Product>): Product {
  return {
    id: 1, url: "https://shop.test/a", store: "shop.test", name: "Mouse", currency: "USD",
    target_price: 50, last_price: 60, alerts_enabled: true, price_selector: null,
    last_checked_at: null, last_error: null, created_at: "2026-11-01T00:00:00Z",
    trend: [], change_7d: null, ...changes,
  };
}

describe("productStatus", () => {
  it.each([
    [{ last_error: "404" }, "Check failed", "warn"],
    [{ last_price: null }, "Waiting", "warn"],
    [{ last_price: 50 }, "Under target", "drop"],
    [{ change_7d: -6.4 }, "Down 6%", "drop"],
    [{ change_7d: 3 }, "Up 3%", "rise"],
    [{ change_7d: 1 }, "Stable", "neutral"],
  ])("%o → %s", (changes, label, tone) => {
    expect(productStatus(product(changes))).toEqual({ label, tone });
  });
});
