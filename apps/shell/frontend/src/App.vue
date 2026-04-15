<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();
const authFailed = ref(false);

onMounted(async () => {
  try {
    await authStore.init();
  } catch (e) {
    console.error("Auth init failed:", e);
    authFailed.value = true;
  }
});
</script>

<template>
  <div v-if="authStore.isAuthenticated">
    <router-view />
  </div>
  <div v-else-if="authFailed" class="flex items-center justify-center h-screen">
    <div class="text-center">
      <p class="text-destructive font-medium mb-2">Authentication failed</p>
      <p class="text-muted-foreground text-sm mb-4">Could not connect to Keycloak. Check that it's running at {{ $env?.VITE_KEYCLOAK_URL }}.</p>
      <button class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm" @click="authStore.init()">
        Retry
      </button>
    </div>
  </div>
  <div v-else class="flex items-center justify-center h-screen">
    <div class="text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-muted-foreground">Authenticating...</p>
    </div>
  </div>
</template>
