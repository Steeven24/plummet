import { useState } from "react";

import { AddProductForm } from "./components/AddProductForm";
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
      <PriceChart product={selected} />
      <ProductTable
        products={products}
        selectedId={selected?.id ?? null}
        onSelect={setSelectedId}
      />
    </Layout>
  );
}
