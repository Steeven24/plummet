/** Percent change from the first to the last price, like -4.1. */
export function percentChange(first: number | undefined, last: number | undefined): number | null {
  if (first === undefined || last === undefined || first === 0) return null;
  return Math.round(((last - first) / first) * 1000) / 10;
}
