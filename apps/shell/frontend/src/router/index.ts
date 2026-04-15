import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import AppLayout from "../layouts/AppLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import RemoteAppView from "../views/RemoteAppView.vue";

// Lazy-load remote route definitions
async function loadRemoteRoutes(remoteName: string): Promise<RouteRecordRaw[]> {
  const remoteModules: Record<string, () => Promise<{ routes: RouteRecordRaw[] }>> = {
    example1: () => import("example1/routes"),
  };

  const loader = remoteModules[remoteName];
  if (!loader) return [];

  const mod = await loader();
  return mod.routes;
}

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      component: AppLayout,
      children: [
        {
          path: "",
          name: "dashboard",
          component: DashboardView,
        },
        {
          path: "app/example1/:pathMatch(.*)*",
          name: "mfe-example1",
          component: RemoteAppView,
          meta: { remoteName: "example1" },
        },
      ],
    },
  ],
});

// Dynamically add remote routes on first navigation
let remoteRoutesLoaded = false;

router.beforeEach(async (to) => {
  if (remoteRoutesLoaded) return;
  if (!to.meta.remoteName) return;

  const remoteName = to.meta.remoteName as string;
  const remoteRoutes = await loadRemoteRoutes(remoteName);

  // Find the parent route and add remote routes as children
  const parentRoute = router.getRoutes().find((r) => r.name === `mfe-${remoteName}`);
  if (parentRoute) {
    for (const route of remoteRoutes) {
      router.addRoute(`mfe-${remoteName}`, route);
    }
    remoteRoutesLoaded = true;

    // Re-navigate to resolve the newly added routes
    return to.fullPath;
  }
});
