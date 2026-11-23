import { type FormEvent, useState } from "react";

import { useUpdateProduct } from "../hooks/mutations";
import { formatPrice, parseAmount } from "../lib/format";
import type { Product } from "../lib/types";

/** Shows the target price. Click it to change it; leave it empty to remove it. */
export function TargetEditor({ product }: { product: Product }) {
  const [editing, setEditing] = useState(false);
  const [text, setText] = useState("");
  const update = useUpdateProduct();

  function start() {
    setText(product.target_price?.toString() ?? "");
    setEditing(true);
  }

  function save(event: FormEvent) {
    event.preventDefault();
    const target = text.trim() ? parseAmount(text) : null;
    if (text.trim() && target === null) return;
    update.mutate(
      { id: product.id, changes: { target_price: target } },
      { onSuccess: () => setEditing(false) },
    );
  }

  if (!editing) {
    return (
      <button
        type="button"
        className="mono"
        title="Change target price"
        onClick={start}
        style={{ padding: 0, border: "none", background: "none", color: "var(--muted)", cursor: "pointer", textAlign: "left" }}
      >
        {formatPrice(product.target_price, product.currency)} ✎
      </button>
    );
  }

  return (
    <form onSubmit={save} style={{ display: "flex", gap: 4 }}>
      <label style={{ flex: 1 }}>
        <span className="sr-only">New target price</span>
        <input
          className="input mono"
          autoFocus
          inputMode="decimal"
          value={text}
          onChange={(event) => setText(event.target.value)}
          onKeyDown={(event) => event.key === "Escape" && setEditing(false)}
          style={{ padding: "5px 8px" }}
        />
      </label>
      <button className="btn btn-icon" type="submit" aria-label="Save target">
        ✓
      </button>
    </form>
  );
}
