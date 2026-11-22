/** "$1,299.99" with the currency, or "1,299.99" if the currency is not known. */
export function formatPrice(value: number | null, currency?: string | null): string {
  if (value === null) return "—";
  try {
    if (currency) {
      return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(value);
    }
  } catch {
    // Not a valid currency code. Show only the number.
  }
  return new Intl.NumberFormat("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    .format(value);
}

/** "↓ 4.1%" or "↑ 2.0%". */
export function formatChange(percent: number | null): string {
  if (percent === null) return "—";
  const arrow = percent <= 0 ? "↓" : "↑";
  return `${arrow} ${Math.abs(percent).toFixed(1)}%`;
}

function minutesBetween(from: Date, to: Date): number {
  return Math.round((to.getTime() - from.getTime()) / 60_000);
}

function humanMinutes(minutes: number): string {
  if (minutes < 60) return `${minutes} min`;
  if (minutes < 60 * 24) return `${Math.round(minutes / 60)} h`;
  return `${Math.round(minutes / (60 * 24))} d`;
}

/** "8 min ago", "3 h ago" or "just now". */
export function timeAgo(iso: string, now = new Date()): string {
  const minutes = minutesBetween(new Date(iso), now);
  return minutes < 1 ? "just now" : `${humanMinutes(minutes)} ago`;
}

/** "in 22 min", or "soon" when the time has passed. */
export function timeUntil(iso: string, now = new Date()): string {
  const minutes = minutesBetween(now, new Date(iso));
  return minutes < 1 ? "soon" : `in ${humanMinutes(minutes)}`;
}

/** Local time like "09:30". */
export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
}
