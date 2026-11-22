import { Layout } from "./components/Layout";

export function App() {
  return (
    <Layout>
      <header id="overview">
        <h1 style={{ margin: 0, fontSize: 24, fontWeight: 500 }}>Overview</h1>
        <p className="muted" style={{ margin: 0 }}>
          Your tracked products and price alerts.
        </p>
      </header>
    </Layout>
  );
}
