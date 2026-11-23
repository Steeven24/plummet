import type { ReactNode } from "react";

import styles from "./Layout.module.css";
import { TelegramStatus } from "./TelegramStatus";
import { ThemeToggle } from "./ThemeToggle";

const SECTIONS = [
  { id: "overview", label: "Overview" },
  { id: "products", label: "Products" },
  { id: "alerts", label: "Alerts" },
  { id: "cron", label: "Scheduled job" },
];

function Logo() {
  return (
    <span className={styles.logo} aria-hidden="true">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#5EE3B5"
        strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 7l6 6 4-4 8 8" />
        <path d="M14 17h7v-7" />
      </svg>
    </span>
  );
}

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <Logo />
          Plummet
        </div>
        <nav className={styles.nav} aria-label="Sections">
          {SECTIONS.map((section) => (
            <a key={section.id} className={styles.navLink} href={`#${section.id}`}>
              {section.label}
            </a>
          ))}
        </nav>
        <div className={styles.footer} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <TelegramStatus />
          <ThemeToggle />
        </div>
      </aside>
      <main className={styles.main}>{children}</main>
    </div>
  );
}
