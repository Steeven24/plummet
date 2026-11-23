import { useAlerts } from "../hooks/queries";
import { formatTime } from "../lib/format";
import { htmlToLines } from "../lib/html";
import styles from "./SidePanels.module.css";

/** The last alerts, shown like Telegram messages. */
export function AlertFeed() {
  const { data: alerts = [] } = useAlerts();

  return (
    <section id="alerts" className={`card ${styles.panel}`} aria-label="Telegram alerts">
      <div className={styles.head}>
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span className={styles.title}>Telegram alerts</span>
          <span className="muted" style={{ fontSize: 12 }}>Last 7 days</span>
        </div>
        <span className="chip primary">{alerts.length}</span>
      </div>
      <div className={styles.feed}>
        {alerts.length === 0 && (
          <p className="muted" style={{ margin: 0, fontSize: 13 }}>
            No alerts yet. You get one when a price drops.
          </p>
        )}
        {alerts.map((alert) => {
          const [title, ...body] = htmlToLines(alert.text);
          return (
            <article key={alert.id} className={styles.bubble}>
              <strong style={{ fontWeight: 500 }}>{title}</strong>
              {body.map((line, index) => (
                <span key={index} style={{ color: "var(--ink-2)" }}>{line}</span>
              ))}
              {!alert.delivered && (
                <span className="chip warn" style={{ alignSelf: "flex-start", marginTop: 4 }}>
                  Not sent: {alert.error ?? "unknown error"}
                </span>
              )}
              <span className={styles.time}>{formatTime(alert.created_at)}</span>
            </article>
          );
        })}
      </div>
    </section>
  );
}
