import type { Product } from "../lib/types";
import { ProductRow } from "./ProductRow";
import styles from "./ProductTable.module.css";

interface Props {
  products: Product[];
  selectedId: number | null;
  onSelect: (id: number) => void;
}

const COLUMNS = ["Product", "Trend (30 d)", "Price", "Target", "Status", ""];

export function ProductTable({ products, selectedId, onSelect }: Props) {
  return (
    <section id="products" className={`card ${styles.panel}`} aria-label="Tracked products">
      <div className={styles.head}>
        <span>Tracked products</span>
        <span className="muted" style={{ fontSize: 13, fontWeight: 400 }}>
          {products.length} {products.length === 1 ? "product" : "products"}
        </span>
      </div>
      {products.length === 0 ? (
        <p className={styles.empty}>
          No products yet. Paste a product link above, or send /add to the Telegram bot.
        </p>
      ) : (
        <div className={styles.scroll}>
          <div className={styles.table} role="table">
            <div className={`${styles.row} ${styles.header}`} role="row">
              {COLUMNS.map((column) => (
                <span key={column} role="columnheader">{column}</span>
              ))}
            </div>
            {products.map((product) => (
              <ProductRow
                key={product.id}
                product={product}
                selected={product.id === selectedId}
                onSelect={() => onSelect(product.id)}
              />
            ))}
          </div>
        </div>
      )}
    </section>
  );
}
