import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import federation from "@originjs/vite-plugin-federation";
import { resolve } from "path";

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: "example1",
      filename: "remoteEntry.js",
      exposes: {
        "./routes": "./src/routes.ts",
      },
      shared: ["vue", "vue-router", "pinia"],
    }),
  ],
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "@common": resolve(__dirname, "../../../common/templates/frontend/src"),
    },
    dedupe: ["vue", "pinia", "vue-router"],
  },
  build: {
    target: "esnext",
    cssCodeSplit: false,
  },
  server: {
    port: 5174,
    allowedHosts: true,
    cors: true,
    watch: {
      usePolling: true,
      interval: 1000,
    },
  },
  preview: {
    port: 5174,
    cors: true,
    allowedHosts: true,
  },
});
