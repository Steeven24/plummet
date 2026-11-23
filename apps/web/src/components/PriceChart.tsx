import { useState } from "react";

import { useHistory } from "../hooks/queries";
import { buildChart } from "../lib/chart";
import { formatChange, formatPrice } from "../lib/format";
import { percentChange } from "../lib/stats";
import type { Product } from "../lib/types";
import { ChartBody } from "./ChartBody";
import { CHART_HEIGHT, CHART_WIDTH } from "./ChartSvg";
import styles from "./PriceChart.module.css";
import { RangePicker } from "./RangePicker";

const RANGES = [7, 30, 90];

const shortDate = (iso: string) =>
  new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });

export function PriceChart({ product }: { product: Product | null }) {
  const [days, setDays] = useState(30);
  const { data: points = [] } = useHistory(product?.id ?? null, days);

  if (!product) {
    return (
      <section className={`card ${styles.panel}`}>
        <div className={styles.empty}>Add a product to see its price chart.</div>
      </section>
    );
  }

  const prices = points.map((point) => point.price);
  const chart = buildChart(prices, product.target_price, CHART_WIDTH, CHART_HEIGHT);
  const change = percentChange(prices[0], prices[prices.length - 1]);
  const money = (value: number | null) => formatPrice(value, product.currency);
  const dates = points.length
    ? [points[0], points[Math.floor((points.length - 1) / 2)], points[points.length - 1]]
    : [];

  return (
    <section className={`card ${styles.panel}`} aria-label="Price chart">
      <div className={styles.top}>
        <div>
          <div className="muted" style={{ fontSize: 13 }}>{product.store}</div>
          <div className={styles.name}>{product.name ?? product.url}</div>
          <div className={`mono ${styles.price}`}>
            {money(product.last_price)}
            <span
              className={styles.change}
              style={{ color: change !== null && change > 0 ? "var(--rise)" : "var(--drop)" }}
            >
              {formatChange(change)} in {days} days
            </span>
          </div>
        </div>
        <RangePicker options={RANGES} value={days} onChange={setDays} />
      </div>
      {prices.length ? (
        <ChartBody chart={chart} dates={dates.map((p) => shortDate(p.checked_at))} money={money} />
      ) : (
        <div className={styles.empty}>No prices yet. They appear after the next check.</div>
      )}
      <div className={styles.legend}>
        <span>━ Price</span>
        <span style={{ color: "var(--drop)" }}>┅ Target {money(product.target_price)}</span>
        <span className="muted">Lowest in period {money(chart.min)}</span>
      </div>
    </section>
  );
}
