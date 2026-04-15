<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useAuthStore } from "../stores/auth";

defineProps<{
  src: string;
}>();

const authStore = useAuthStore();
const iframeRef = ref<HTMLIFrameElement | null>(null);

function sendTokenToIframe(): void {
  if (iframeRef.value?.contentWindow) {
    const token = authStore.getToken();
    if (token) {
      iframeRef.value.contentWindow.postMessage(
        { type: "MFE_AUTH_TOKEN", token },
        "*"
      );
    }
  }
}

onMounted(() => {
  // Listen for token requests from iframe
  window.addEventListener("message", (event: MessageEvent) => {
    if (event.data?.type === "MFE_REQUEST_TOKEN") {
      sendTokenToIframe();
    }
  });
});

// Re-send token when it changes
watch(() => authStore.token, () => {
  sendTokenToIframe();
});
</script>

<template>
  <iframe
    ref="iframeRef"
    :src="src"
    class="w-full h-full border-0"
    @load="sendTokenToIframe"
  />
</template>
