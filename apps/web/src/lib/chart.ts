/** Math to draw a price chart in an SVG box. Kept apart from React to test it. */

export interface ChartData {
  line: string; // SVG path of the price line
  area: string; // SVG path of the area under the line
  targetY: number | null; // y position of the target line
  yTicks: number[]; // prices for the labels on the left, top to bottom
  min: number | null; // lowest price in the period
}

export const EMPTY_CHART: ChartData = { line: "", area: "", targetY: null, yTicks: [], min: null };

export function buildChart(
  prices: number[],
  target: number | null,
  width: number,
  height: number,
): ChartData {
  if (prices.length === 0) return EMPTY_CHART;

  // Include the target, so its line is always inside the chart.
  const values = target === null ? prices : [...prices, target];
  const low = Math.min(...values);
  const high = Math.max(...values);
  const pad = (high - low) * 0.12 || Math.max(high * 0.05, 1);
  const bottom = low - pad;
  const top = high + pad;

  const y = (value: number) => +(height - ((value - bottom) / (top - bottom)) * height).toFixed(1);
  const x = (index: number) =>
    prices.length === 1 ? width / 2 : +((index / (prices.length - 1)) * width).toFixed(1);

  const points = prices.map((price, index) => `${x(index)},${y(price)}`);
  const firstX = x(0);
  const lastX = x(prices.length - 1);

  return {
    line: `M${points.join(" L")}`,
    area: `M${firstX},${height} L${points.join(" L")} L${lastX},${height} Z`,
    targetY: target === null ? null : y(target),
    yTicks: [0, 1, 2, 3].map((step) => top - ((top - bottom) * step) / 3),
    min: Math.min(...prices),
  };
}

/** Small line for the product table. */
export function sparkline(prices: number[], width: number, height: number): string {
  if (prices.length < 2) return "";
  const low = Math.min(...prices);
  const range = Math.max(...prices) - low || 1;
  return prices
    .map((price, index) => {
      const x = (index / (prices.length - 1)) * (width - 2) + 1;
      const y = height - 2 - ((price - low) / range) * (height - 4);
      return `${index ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}
