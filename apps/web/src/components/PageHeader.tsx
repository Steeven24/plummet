import type { ReactNode } from "react";

import { useCron, useOverview } from "../hooks/queries";
import { timeAgo, timeUntil } from "../lib/format";

function CheckInfo() {
  const { data: cron } = useCron();
  if (!cron?.last_run) return <>No checks yet. Run the worker or wait for cron.</>;
  const next = cron.next_run_at ? ` · next ${timeUntil(cron.next_run_at)}` : "";
  return <>Last check {timeAgo(cron.last_run.started_at)}{next}</>;
}

/** Page title, check times and a warning when the API does not answer. */
export function PageHeader({ children }: { children?: ReactNode }) {
  const { isError } = useOverview();
  return (
    <header id="overview" style={{ display: "flex", flexDirection: "column", gap: 12 }}>
      {isError && (
        <div role="alert" className="chip warn" style={{ alignSelf: "flex-start" }}>
          Cannot reach the API. Start it with “make api”.
        </div>
      )}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "flex-end",
          justifyContent: "space-between",
          gap: 16,
        }}
      >
        <div>
          <h1 style={{ margin: 0, fontSize: 24, fontWeight: 500 }}>Overview</h1>
          <p className="muted" style={{ margin: 0, fontSize: 14 }}>
            <CheckInfo />
          </p>
        </div>
        {children}
      </div>
    </header>
  );
}
