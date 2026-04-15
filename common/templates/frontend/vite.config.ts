import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { resolve } from "path";

/**
 * Base Vite configuration for MFE apps.
 * Individual apps should extend this config.
 */
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@common": resolve(__dirname, "src"),
    },
  },
});
