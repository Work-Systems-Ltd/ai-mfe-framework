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
  },
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/internal": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
      "/apps": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
