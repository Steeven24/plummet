/// <reference types="vitest/config" />
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// In development, calls to /api go to the Python API.
const apiUrl = process.env.PLUMMET_API_URL ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": apiUrl },
  },
  test: {
    include: ["src/**/*.test.ts"],
  },
});
