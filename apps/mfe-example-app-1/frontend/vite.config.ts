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
  },
  server: {
    port: 5174,
  },
});
