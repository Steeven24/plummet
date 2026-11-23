import { describe, expect, it } from "vitest";

import { buildChart, EMPTY_CHART, sparkline } from "./chart";

describe("buildChart", () => {
  it("returns an empty chart without prices", () => {
    expect(buildChart([], 10, 600, 200)).toEqual(EMPTY_CHART);
  });

  it("draws the line from left to right", () => {
    const chart = buildChart([100, 80, 90], null, 600, 200);

    expect(chart.line.startsWith("M0,")).toBe(true);
    expect(chart.line).toContain(" L300,");
    expect(chart.line).toContain(" L600,");
    expect(chart.area.endsWith("L600,200 Z")).toBe(true);
    expect(chart.min).toBe(80);
  });

  it("keeps the target inside the chart", () => {
    const chart = buildChart([100, 90], 50, 600, 200);

    expect(chart.targetY).toBeGreaterThan(0);
    expect(chart.targetY).toBeLessThan(200);
    expect(chart.yTicks[3]).toBeLessThan(50);
  });

  it("works with one price", () => {
    expect(buildChart([42], null, 600, 200).line).toMatch(/^M300,/);
  });
});

describe("sparkline", () => {
  it("needs two prices", () => {
    expect(sparkline([5], 90, 28)).toBe("");
    expect(sparkline([5, 4, 6], 90, 28).split(" ")).toHaveLength(3);
  });
});
