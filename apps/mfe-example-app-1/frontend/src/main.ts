/**
 * Standalone bootstrap for the example app.
 * Used when running the app independently (not via Module Federation).
 * When loaded via federation, only routes.ts is imported by the shell.
 */
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import { router } from "./router";
import "@common/styles/globals.css";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");
