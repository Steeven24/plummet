import { useQuery } from "@tanstack/react-query";

import { api } from "../lib/api";

// One place for the query keys, so changes can refresh the right data.
export const keys = {
  products: ["products"] as const,
  overview: ["overview"] as const,
  history: (id: number, days: number) => ["history", id, days] as const,
  alerts: ["alerts"] as const,
  cron: ["cron"] as const,
  logs: ["logs"] as const,
};

export const useProducts = () => useQuery({ queryKey: keys.products, queryFn: api.products });

export const useOverview = () => useQuery({ queryKey: keys.overview, queryFn: api.overview });

export const useHistory = (id: number | null, days: number) =>
  useQuery({
    queryKey: keys.history(id ?? 0, days),
    queryFn: () => api.history(id!, days),
    enabled: id !== null,
  });

export const useAlerts = () => useQuery({ queryKey: keys.alerts, queryFn: api.alerts });

export const useCron = () => useQuery({ queryKey: keys.cron, queryFn: api.cron });

export const useLogs = () => useQuery({ queryKey: keys.logs, queryFn: api.logs });
