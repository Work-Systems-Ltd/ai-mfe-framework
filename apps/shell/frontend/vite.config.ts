import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

const backendTarget = process.env.PROXY_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "@common": resolve(__dirname, "../../../common/templates/frontend/src"),
    },
    dedupe: ["vue", "pinia", "vue-router", "keycloak-js"],
  },
  optimizeDeps: {
    include: ["keycloak-js", "vue", "pinia", "vue-router"],
  },
  server: {
    port: 5173,
    allowedHosts: true,
    watch: {
      usePolling: true,
      interval: 1000,
    },
    proxy: {
      "/api": {
        target: backendTarget,
        changeOrigin: true,
      },
      "/internal": {
        target: backendTarget,
        changeOrigin: true,
      },
      // In dev: proxy example app frontend directly to its Vite dev server
      // and API calls to the shell backend (which proxies to the app backend)
      "/apps/example1/api": {
        target: backendTarget,
        changeOrigin: true,
      },
      "/apps/example1": {
        target: process.env.EXAMPLE1_FRONTEND || "http://localhost:5174",
        changeOrigin: true,
      },
      // Fallback: any other /apps/* goes to shell backend
      "/apps": {
        target: backendTarget,
        changeOrigin: true,
      },
    },
  },
});
