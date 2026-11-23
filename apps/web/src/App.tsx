import { useState } from "react";

import { Layout } from "./components/Layout";
import { PageHeader } from "./components/PageHeader";
import { PriceChart } from "./components/PriceChart";
import { StatCards } from "./components/StatCards";
import { useProducts } from "./hooks/queries";

export function App() {
  const { data: products = [] } = useProducts();
  // The product table will change the selected product.
  const [selectedId] = useState<number | null>(null);
  const selected = products.find((p) => p.id === selectedId) ?? products[0] ?? null;

  return (
    <Layout>
      <PageHeader />
      <StatCards />
      <PriceChart product={selected} />
    </Layout>
  );
}
