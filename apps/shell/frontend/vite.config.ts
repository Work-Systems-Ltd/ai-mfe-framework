import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "@common": resolve(__dirname, "../../../common/templates/frontend/src"),
    },
    // Ensure imports from @common resolve deps from this app's node_modules
    dedupe: ["vue", "pinia", "vue-router", "keycloak-js"],
  },
  optimizeDeps: {
    include: ["keycloak-js", "vue", "pinia", "vue-router"],
  },
  server: {
    port: 5173,
    allowedHosts: true,
    proxy: {
      "/api": {
        target: process.env.PROXY_TARGET || "http://localhost:8000",
        changeOrigin: true,
      },
      "/internal": {
        target: process.env.PROXY_TARGET || "http://localhost:8000",
        changeOrigin: true,
      },
      "/apps": {
        target: process.env.PROXY_TARGET || "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
