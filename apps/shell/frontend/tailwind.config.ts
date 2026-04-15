import baseConfig from "../../../common/templates/frontend/tailwind.config";
import type { Config } from "tailwindcss";

const config: Config = {
  ...baseConfig,
  content: [
    "./index.html",
    "./src/**/*.{vue,ts}",
    "../../../common/templates/frontend/src/**/*.{vue,ts}",
  ],
};

export default config;
