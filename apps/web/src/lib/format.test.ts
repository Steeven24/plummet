import { describe, expect, it } from "vitest";

import { formatChange, formatPrice, timeAgo, timeUntil } from "./format";

describe("formatPrice", () => {
  it("shows the currency", () => {
    expect(formatPrice(1299.9, "USD")).toBe("$1,299.90");
    expect(formatPrice(2549, "MXN")).toBe("MX$2,549.00");
  });

  it("works without a valid currency", () => {
    expect(formatPrice(5, null)).toBe("5.00");
    expect(formatPrice(5, "???")).toBe("5.00");
    expect(formatPrice(null)).toBe("—");
  });
});

describe("formatChange", () => {
  it("shows an arrow", () => {
    expect(formatChange(-4.12)).toBe("↓ 4.1%");
    expect(formatChange(2)).toBe("↑ 2.0%");
    expect(formatChange(null)).toBe("—");
  });
});

describe("relative times", () => {
  const now = new Date("2026-11-12T10:00:00Z");

  it("timeAgo", () => {
    expect(timeAgo("2026-11-12T09:52:00Z", now)).toBe("8 min ago");
    expect(timeAgo("2026-11-12T07:00:00Z", now)).toBe("3 h ago");
    expect(timeAgo("2026-11-10T10:00:00Z", now)).toBe("2 d ago");
    expect(timeAgo("2026-11-12T10:00:00Z", now)).toBe("just now");
  });

  it("timeUntil", () => {
    expect(timeUntil("2026-11-12T10:22:00Z", now)).toBe("in 22 min");
    expect(timeUntil("2026-11-12T09:00:00Z", now)).toBe("soon");
  });
});
