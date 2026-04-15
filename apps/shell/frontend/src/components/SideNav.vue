<script setup lang="ts">
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import type { RegisteredApp } from "../stores/apps";
import type { AuthUser } from "@common/composables/useAuth";

const props = defineProps<{
  apps: RegisteredApp[];
  user: AuthUser | null | undefined;
}>();

const emit = defineEmits<{
  logout: [];
}>();

const route = useRoute();
const router = useRouter();

const healthyApps = computed(() => props.apps.filter((app) => app.healthy));

function navigateToApp(appName: string, path: string): void {
  router.push({ name: "mfe-app", params: { appName, pathMatch: path.replace(/^\//, "").split("/") } });
}

function isActiveApp(appName: string): boolean {
  return route.params.appName === appName;
}
</script>

<template>
  <aside class="w-64 border-r bg-card flex flex-col h-full">
    <!-- Logo / title -->
    <div class="p-4 border-b">
      <h1 class="text-lg font-semibold">
        <router-link to="/" class="hover:text-primary">MFE Framework</router-link>
      </h1>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto p-2">
      <!-- Dashboard -->
      <router-link
        to="/"
        class="flex items-center gap-2 px-3 py-2 rounded-md text-sm hover:bg-accent transition-colors"
        :class="{ 'bg-accent': route.path === '/' }"
      >
        Dashboard
      </router-link>

      <!-- Registered apps -->
      <div v-for="app in healthyApps" :key="app.name" class="mt-2">
        <div class="px-3 py-1 text-xs font-medium text-muted-foreground uppercase tracking-wider">
          {{ app.display_name }}
        </div>

        <template v-for="link in app.sidebar_links" :key="link.path">
          <button
            class="w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm hover:bg-accent transition-colors text-left"
            :class="{ 'bg-accent': isActiveApp(app.name) }"
            @click="navigateToApp(app.name, link.path)"
          >
            {{ link.label }}
          </button>

          <!-- Sublinks -->
          <button
            v-for="sublink in link.sublinks"
            :key="sublink.path"
            class="w-full flex items-center gap-2 px-3 py-2 pl-8 rounded-md text-sm hover:bg-accent transition-colors text-left text-muted-foreground"
            @click="navigateToApp(app.name, sublink.path)"
          >
            {{ sublink.label }}
          </button>
        </template>
      </div>
    </nav>

    <!-- User section -->
    <div class="border-t p-4">
      <div class="flex items-center justify-between">
        <div class="text-sm">
          <p class="font-medium">{{ user?.username ?? "Unknown" }}</p>
          <p class="text-muted-foreground text-xs">{{ user?.email }}</p>
        </div>
        <button
          class="text-sm text-muted-foreground hover:text-foreground transition-colors"
          @click="emit('logout')"
        >
          Logout
        </button>
      </div>
    </div>
  </aside>
</template>
