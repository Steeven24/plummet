import { sparkline } from "../lib/chart";
import { formatPrice } from "../lib/format";
import { productStatus } from "../lib/status";
import type { Product } from "../lib/types";
import styles from "./ProductTable.module.css";
import { RowActions } from "./RowActions";
import { TargetEditor } from "./TargetEditor";

interface Props {
  product: Product;
  selected: boolean;
  onSelect: () => void;
}

export function ProductRow({ product, selected, onSelect }: Props) {
  const status = productStatus(product);
  const trend = product.trend;
  const goingDown = trend.length > 1 && trend[trend.length - 1] <= trend[0];

  return (
    <div className={`${styles.row} ${selected ? styles.selected : ""}`}>
      <button
        type="button"
        className={styles.product}
        onClick={onSelect}
        aria-pressed={selected}
        title={product.last_error ?? product.url}
      >
        <span className={styles.name}>{product.name ?? product.url}</span>
        <span className="muted" style={{ fontSize: 12 }}>{product.store}</span>
      </button>
      <svg viewBox="0 0 90 28" width="90" height="28" aria-hidden="true">
        <path
          d={sparkline(trend, 90, 28)}
          fill="none"
          stroke={goingDown ? "var(--drop-line)" : "var(--rise-line)"}
          strokeWidth="1.5"
          strokeLinejoin="round"
        />
      </svg>
      <span className="mono">{formatPrice(product.last_price, product.currency)}</span>
      <TargetEditor product={product} />
      <span>
        <span className={`chip ${status.tone}`}>{status.label}</span>
      </span>
      <span className={styles.actions}>
        <RowActions product={product} />
      </span>
    </div>
  );
}
