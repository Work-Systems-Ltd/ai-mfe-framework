<script setup lang="ts">
import { onMounted } from "vue";
import { useAuthStore } from "./stores/auth";

const authStore = useAuthStore();

onMounted(async () => {
  await authStore.init();
});
</script>

<template>
  <div v-if="authStore.isAuthenticated">
    <router-view />
  </div>
  <div v-else class="flex items-center justify-center h-screen">
    <div class="text-center">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
      <p class="text-muted-foreground">Authenticating...</p>
    </div>
  </div>
</template>
