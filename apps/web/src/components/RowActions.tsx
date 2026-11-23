import { useState } from "react";

import { useDeleteProduct, useUpdateProduct } from "../hooks/mutations";
import type { Product } from "../lib/types";
import { BellIcon, BellOffIcon, TrashIcon } from "./Icons";

/** Bell to turn alerts on or off, and a delete button that asks first. */
export function RowActions({ product }: { product: Product }) {
  const [confirming, setConfirming] = useState(false);
  const update = useUpdateProduct();
  const remove = useDeleteProduct();
  const on = product.alerts_enabled;

  if (confirming) {
    return (
      <>
        <button className="btn btn-ghost" type="button" onClick={() => setConfirming(false)}>
          Keep
        </button>
        <button
          className="btn"
          type="button"
          style={{ background: "var(--rise-line)", color: "#fff" }}
          onClick={() => remove.mutate(product.id)}
        >
          Delete
        </button>
      </>
    );
  }

  return (
    <>
      <button
        className="btn btn-ghost btn-icon"
        type="button"
        aria-pressed={on}
        aria-label={on ? "Turn alerts off" : "Turn alerts on"}
        title={on ? "Alerts on" : "Alerts off"}
        onClick={() => update.mutate({ id: product.id, changes: { alerts_enabled: !on } })}
        style={{ color: on ? "var(--primary)" : "var(--muted)" }}
      >
        {on ? <BellIcon /> : <BellOffIcon />}
      </button>
      <button
        className="btn btn-ghost btn-icon"
        type="button"
        aria-label={`Delete ${product.name ?? product.store}`}
        onClick={() => setConfirming(true)}
      >
        <TrashIcon />
      </button>
    </>
  );
}
