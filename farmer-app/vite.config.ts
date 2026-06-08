import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// The farmer app talks to the FastAPI backend. During development we proxy
// /api -> http://127.0.0.1:8000 so there are no CORS surprises.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
