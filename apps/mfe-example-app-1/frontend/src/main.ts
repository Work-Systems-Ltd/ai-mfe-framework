import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import { router } from "./router";
import "@common/styles/globals.css";
import { setTokenProvider } from "@common/lib/api";

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.mount("#app");

// Listen for auth token from parent shell via postMessage
window.addEventListener("message", (event: MessageEvent) => {
  if (event.data?.type === "MFE_AUTH_TOKEN") {
    setTokenProvider(() => event.data.token);
  }
});

// Request token from parent shell
window.parent.postMessage({ type: "MFE_REQUEST_TOKEN" }, "*");
