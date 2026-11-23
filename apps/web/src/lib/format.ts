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

/** Read what the user typed: "99.90", "99,90", "1,299.99" or "1.299,99". */
export function parseAmount(text: string): number | null {
  const clean = text.replace(/[^\d.,]/g, "");
  if (!clean) return null;
  const lastDot = clean.lastIndexOf(".");
  const lastComma = clean.lastIndexOf(",");
  const decimalMark = lastDot > lastComma ? "." : ",";
  const parts = clean.split(decimalMark);
  // A single mark with 3 digits after it is a thousands mark ("2.549").
  const onlyThousands =
    (lastDot === -1 || lastComma === -1) && parts.length === 2 && parts[1].length === 3;
  const normal = onlyThousands
    ? clean.replace(/[.,]/g, "")
    : clean.replace(decimalMark === "." ? /,/g : /\./g, "").replace(",", ".");
  const value = Number(normal);
  return Number.isFinite(value) && value > 0 ? value : null;
}
