import { type FormEvent, useState } from "react";

import { useAddProduct } from "../hooks/mutations";
import { ApiError } from "../lib/api";

function errorText(error: unknown): string {
  if (error instanceof ApiError && error.status === 422) {
    return "Please check the link (it must start with https://) and the price.";
  }
  return error instanceof Error ? error.message : "Could not add the product.";
}

/** Paste a product link (and an optional target price) to start tracking it. */
export function AddProductForm() {
  const [url, setUrl] = useState("");
  const [target, setTarget] = useState("");
  const add = useAddProduct();

  function submit(event: FormEvent) {
    event.preventDefault();
    if (!url.trim()) return;
    const targetPrice = target.trim() ? Number(target.replace(",", ".")) : null;
    add.mutate(
      { url: url.trim(), target_price: targetPrice },
      { onSuccess: () => (setUrl(""), setTarget("")) },
    );
  }

  return (
    <form onSubmit={submit} style={{ display: "flex", flexDirection: "column", gap: 6, flex: "0 1 520px" }}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        <label style={{ flex: "1 1 240px" }}>
          <span className="sr-only">Product link</span>
          <input
            className="input"
            type="url"
            required
            placeholder="Paste a product link…"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
          />
        </label>
        <label style={{ flex: "0 1 120px" }}>
          <span className="sr-only">Target price (optional)</span>
          <input
            className="input mono"
            inputMode="decimal"
            placeholder="Target"
            value={target}
            onChange={(event) => setTarget(event.target.value)}
          />
        </label>
        <button className="btn" type="submit" disabled={add.isPending}>
          {add.isPending ? "Adding…" : "Track"}
        </button>
      </div>
      {add.isError && (
        <span role="alert" style={{ color: "var(--rise)", fontSize: 13 }}>
          {errorText(add.error)}
        </span>
      )}
    </form>
  );
}
