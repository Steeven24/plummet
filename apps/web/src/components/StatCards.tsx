import { useOverview } from "../hooks/queries";
import { formatPrice } from "../lib/format";
import styles from "./StatCards.module.css";

interface Stat {
  label: string;
  value: string;
  note: string;
  good?: boolean;
}

export function StatCards() {
  const { data } = useOverview();
  const plural = (count: number, word: string) => `${count} ${word}${count === 1 ? "" : "s"}`;

  const stats: Stat[] = [
    {
      label: "Tracked products",
      value: data ? String(data.products) : "–",
      note: data ? plural(data.stores, "store") : "",
    },
    {
      label: "Under target price",
      value: data ? String(data.below_target) : "–",
      note: "Good time to buy",
      good: !!data?.below_target,
    },
    {
      label: "Alerts this week",
      value: data ? String(data.alerts_week) : "–",
      note: data ? `${data.alerts_today} today` : "",
    },
    {
      label: "Possible savings",
      value: data ? formatPrice(data.savings, data.currency) : "–",
      note: "vs. 30-day high",
      good: !!data?.savings,
    },
  ];

  return (
    <section className={styles.grid} aria-label="Summary">
      {stats.map((stat) => (
        <div key={stat.label} className={`card ${styles.stat}`}>
          <span className={styles.label}>{stat.label}</span>
          <span className={`mono ${styles.value} ${stat.good ? styles.good : ""}`}>
            {stat.value}
          </span>
          <span className={styles.note}>{stat.note}</span>
        </div>
      ))}
    </section>
  );
}
