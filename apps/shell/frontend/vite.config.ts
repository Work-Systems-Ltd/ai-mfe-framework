import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import federation from "@originjs/vite-plugin-federation";
import { resolve } from "path";

const backendTarget = process.env.PROXY_TARGET || "http://localhost:8000";
const example1Remote = process.env.EXAMPLE1_REMOTE_URL || "http://localhost:5174";

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: "shell",
      remotes: {
        example1: {
          external: `${example1Remote}/assets/remoteEntry.js`,
          format: "esm",
          from: "vite",
        },
      },
      shared: ["vue", "vue-router", "pinia"],
    }),
  ],
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
  build: {
    target: "esnext",
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
      // API calls to sub-apps go through shell backend
      "/apps/example1/api": {
        target: backendTarget,
        changeOrigin: true,
      },
    },
  },
});
