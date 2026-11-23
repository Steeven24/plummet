import { useOverview } from "../hooks/queries";

/** Small box in the sidebar: is the Telegram bot set up? */
export function TelegramStatus() {
  const { data } = useOverview();
  if (!data) return null;
  const on = data.telegram_enabled;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 4,
        padding: 12,
        border: "1px solid var(--line)",
        borderRadius: "var(--r-md)",
        background: "var(--surface-2)",
        fontSize: 13,
      }}
    >
      <span style={{ display: "flex", alignItems: "center", gap: 8, fontWeight: 500 }}>
        <span
          aria-hidden="true"
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background: on ? "var(--drop-line)" : "var(--rise-line)",
          }}
        />
        {on ? "Telegram alerts on" : "Telegram not set up"}
      </span>
      <span className="muted" style={{ fontSize: 12 }}>
        {on ? "Alerts go to your private chat" : "Add the bot token and chat ID to .env"}
      </span>
    </div>
  );
}
