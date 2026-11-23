import { useMutation, useQueryClient } from "@tanstack/react-query";

import { api, type NewProduct, type ProductChanges } from "../lib/api";
import { keys } from "./queries";

/** After a change, reload the product list and the summary numbers. */
function useRefresh() {
  const client = useQueryClient();
  return () => {
    client.invalidateQueries({ queryKey: keys.products });
    client.invalidateQueries({ queryKey: keys.overview });
  };
}

export function useAddProduct() {
  const refresh = useRefresh();
  return useMutation({
    mutationFn: (data: NewProduct) => api.addProduct(data),
    onSuccess: refresh,
  });
}

export function useUpdateProduct() {
  const refresh = useRefresh();
  return useMutation({
    mutationFn: ({ id, changes }: { id: number; changes: ProductChanges }) =>
      api.updateProduct(id, changes),
    onSuccess: refresh,
  });
}

export function useDeleteProduct() {
  const refresh = useRefresh();
  return useMutation({
    mutationFn: (id: number) => api.deleteProduct(id),
    onSuccess: refresh,
  });
}
