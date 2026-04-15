import { defineStore } from "pinia";
import { ref } from "vue";
import { apiFetch } from "@common/lib/api";

export interface SidebarSubLink {
  label: string;
  path: string;
  icon?: string;
}

export interface SidebarLink {
  label: string;
  path: string;
  icon?: string;
  sublinks: SidebarSubLink[];
}

export interface RegisteredApp {
  name: string;
  display_name: string;
  frontend_url: string;
  backend_url: string;
  path_prefix: string;
  sidebar_links: SidebarLink[];
  healthy: boolean;
  registered_at: string;
}

export const useAppsStore = defineStore("apps", () => {
  const apps = ref<RegisteredApp[]>([]);
  const loading = ref(false);

  async function fetchApps(): Promise<void> {
    loading.value = true;
    try {
      apps.value = await apiFetch<RegisteredApp[]>("/api/apps");
    } finally {
      loading.value = false;
    }
  }

  return { apps, loading, fetchApps };
});
