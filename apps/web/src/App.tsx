import { useState } from "react";

import styles from "./App.module.css";
import { AddProductForm } from "./components/AddProductForm";
import { AlertFeed } from "./components/AlertFeed";
import { CronCard } from "./components/CronCard";
import { Layout } from "./components/Layout";
import { PageHeader } from "./components/PageHeader";
import { PriceChart } from "./components/PriceChart";
import { ProductTable } from "./components/ProductTable";
import { StatCards } from "./components/StatCards";
import { useProducts } from "./hooks/queries";

export function App() {
  const { data: products = [] } = useProducts();
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const selected = products.find((p) => p.id === selectedId) ?? products[0] ?? null;

  return (
    <Layout>
      <PageHeader>
        <AddProductForm />
      </PageHeader>
      <StatCards />
      <div className={styles.columns}>
        <div className={styles.wide}>
          <PriceChart product={selected} />
          <ProductTable
            products={products}
            selectedId={selected?.id ?? null}
            onSelect={setSelectedId}
          />
        </div>
        <div className={styles.side}>
          <AlertFeed />
          <CronCard />
        </div>
      </div>
    </Layout>
  );
}
