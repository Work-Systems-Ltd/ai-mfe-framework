<script setup lang="ts">
import { onMounted } from "vue";
import SideNav from "../components/SideNav.vue";
import { useAppsStore } from "../stores/apps";
import { useAuthStore } from "../stores/auth";

const appsStore = useAppsStore();
const authStore = useAuthStore();

onMounted(async () => {
  await appsStore.fetchApps();
});
</script>

<template>
  <div class="flex h-screen">
    <!-- Sidebar -->
    <SideNav
      :apps="appsStore.apps"
      :user="authStore.user"
      @logout="authStore.logout"
    />

    <!-- Main content area -->
    <main class="flex-1 overflow-auto bg-background">
      <router-view />
    </main>
  </div>
</template>
