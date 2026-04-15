import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

export default defineConfig({
  plugins: [vue()],
  base: "/apps/example1/",
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
      "@common": resolve(__dirname, "../../../common/templates/frontend/src"),
    },
    dedupe: ["vue", "pinia", "vue-router"],
  },
  optimizeDeps: {
    include: ["vue", "pinia", "vue-router"],
  },
  server: {
    port: 5174,
    allowedHosts: true,
    hmr: {
      host: "localhost",
      port: 5174,
      protocol: "ws",
    },
    watch: {
      // Use polling since inotify doesn't work across Docker bind mounts
      usePolling: true,
      interval: 1000,
    },
  },
});
