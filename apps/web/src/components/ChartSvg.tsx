import type { ChartData } from "../lib/chart";

export const CHART_WIDTH = 600;
export const CHART_HEIGHT = 200;

/** The drawing of the chart: grid, area, price line and target line. */
export function ChartSvg({ chart, label }: { chart: ChartData; label: string }) {
  return (
    <svg
      viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`}
      preserveAspectRatio="none"
      role="img"
      aria-label={label}
      style={{ display: "block", width: "100%", height: CHART_HEIGHT, overflow: "visible" }}
    >
      {[0, 1, 2].map((step) => (
        <line
          key={step}
          x1="0"
          x2={CHART_WIDTH}
          y1={(CHART_HEIGHT / 3) * step}
          y2={(CHART_HEIGHT / 3) * step}
          stroke="var(--line-2)"
        />
      ))}
      <line x1="0" x2={CHART_WIDTH} y1={CHART_HEIGHT} y2={CHART_HEIGHT} stroke="var(--line)" />
      <path d={chart.area} fill="var(--chart-area)" />
      <path
        d={chart.line}
        fill="none"
        stroke="var(--primary)"
        strokeWidth="2"
        strokeLinejoin="round"
        vectorEffect="non-scaling-stroke"
      />
      {chart.targetY !== null && (
        <line
          x1="0"
          x2={CHART_WIDTH}
          y1={chart.targetY}
          y2={chart.targetY}
          stroke="var(--drop-line)"
          strokeWidth="1.5"
          strokeDasharray="5 5"
          vectorEffect="non-scaling-stroke"
        />
      )}
    </svg>
  );
}
