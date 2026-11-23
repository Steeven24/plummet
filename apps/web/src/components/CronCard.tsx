import { useCron, useLogs } from "../hooks/queries";
import type { CronStatus } from "../lib/types";
import styles from "./SidePanels.module.css";

const LEVEL_COLORS: Record<string, string> = {
  INFO: "#9fe6c8",
  WARNING: "#f5c451",
  ERROR: "#ff9b7a",
};

/** "Running", "Late" (cron did not run for a while) or "No runs yet". */
function jobState(cron: CronStatus | undefined, now = Date.now()) {
  if (!cron?.last_run || !cron.next_run_at) return { label: "No runs yet", tone: "warn" };
  const late = now - new Date(cron.next_run_at).getTime() > cron.interval_minutes * 60_000;
  return late ? { label: "Late", tone: "rise" } : { label: "Running", tone: "drop" };
}

export function CronCard() {
  const { data: cron } = useCron();
  const { data: logs = [] } = useLogs();
  const state = jobState(cron);
  const facts: [string, string][] = [
    ["Cron", cron?.schedule ?? "—"],
    ["Rounds (7 days)", cron ? String(cron.runs_week) : "—"],
    ["Success (7 days)", cron?.success_rate != null ? `${cron.success_rate}%` : "—"],
    ["Average time", cron?.avg_seconds != null ? `${cron.avg_seconds} s` : "—"],
  ];

  return (
    <section id="cron" className={`card ${styles.panel}`} aria-label="Scheduled job">
      <div className={styles.head}>
        <span className={styles.title}>Scheduled job</span>
        <span className={`chip ${state.tone}`}>{state.label}</span>
      </div>
      <div className={styles.facts}>
        {facts.map(([label, value]) => (
          <div key={label} style={{ display: "contents" }}>
            <span className="muted">{label}</span>
            <span className="mono">{value}</span>
          </div>
        ))}
      </div>
      <div className={`mono ${styles.logs}`} aria-label="Last log lines">
        {logs.length === 0 && <span>No logs yet.</span>}
        {logs.map((line, index) => (
          <div key={index}>
            <span style={{ opacity: 0.6 }}>{line.time}</span>{" "}
            <span style={{ color: LEVEL_COLORS[line.level] ?? "#8db4e6" }}>{line.level}</span>{" "}
            {line.message}
          </div>
        ))}
      </div>
    </section>
  );
}
