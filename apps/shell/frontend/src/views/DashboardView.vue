<script setup lang="ts">
import { useAppsStore } from "../stores/apps";
import { useAuthStore } from "../stores/auth";

const appsStore = useAppsStore();
const authStore = useAuthStore();
</script>

<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-2">Dashboard</h1>
    <p class="text-muted-foreground mb-8">
      Welcome back, {{ authStore.user?.firstName ?? authStore.user?.username }}.
    </p>

    <!-- Registered apps grid -->
    <h2 class="text-lg font-semibold mb-4">Registered Applications</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="app in appsStore.apps"
        :key="app.name"
        class="border rounded-lg p-4 hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between mb-2">
          <h3 class="font-medium">{{ app.display_name }}</h3>
          <span
            class="text-xs px-2 py-1 rounded-full"
            :class="app.healthy ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
          >
            {{ app.healthy ? "Healthy" : "Unhealthy" }}
          </span>
        </div>
        <p class="text-sm text-muted-foreground">{{ app.path_prefix }}</p>
        <p class="text-xs text-muted-foreground mt-1">
          {{ app.sidebar_links.length }} sidebar link(s)
        </p>
      </div>
    </div>

    <div v-if="appsStore.apps.length === 0" class="text-center py-12 text-muted-foreground">
      <p>No applications registered yet.</p>
      <p class="text-sm mt-1">Apps will appear here once they start and register with the shell.</p>
    </div>
  </div>
</template>
