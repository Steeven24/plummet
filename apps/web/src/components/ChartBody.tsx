import type { ChartData } from "../lib/chart";
import { ChartSvg } from "./ChartSvg";
import styles from "./PriceChart.module.css";

interface Props {
  chart: ChartData;
  dates: string[];
  money: (value: number) => string;
}

/** The chart with the price labels on the left and the dates below. */
export function ChartBody({ chart, dates, money }: Props) {
  return (
    <div className={styles.chart}>
      <div className={`mono ${styles.axis}`} aria-hidden="true">
        {chart.yTicks.map((tick) => (
          <span key={tick}>{money(tick)}</span>
        ))}
      </div>
      <div style={{ minWidth: 0 }}>
        <ChartSvg chart={chart} label="Price over time" />
        <div className={`mono ${styles.dates}`}>
          {dates.map((date, index) => (
            <span key={index}>{date}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
