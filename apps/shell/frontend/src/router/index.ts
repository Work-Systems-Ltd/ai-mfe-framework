import { createRouter, createWebHistory, type RouteRecordRaw } from "vue-router";
import AppLayout from "../layouts/AppLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import RemoteAppView from "../views/RemoteAppView.vue";

// Registry of remote module loaders
const remoteLoaders: Record<string, () => Promise<{ routes: RouteRecordRaw[] }>> = {
  example1: () => import("example1/routes"),
};

// Track which remotes have been loaded
const loadedRemotes = new Set<string>();

// Build initial routes - remote apps get a parent route,
// children are added dynamically on first navigation
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
          path: "app/example1",
          name: "mfe-example1",
          component: RemoteAppView,
          meta: { remoteName: "example1" },
          children: [],
        },
      ],
    },
  ],
});

// Load remote routes before navigation
router.beforeEach(async (to) => {
  // Check if navigating to a remote app that hasn't been loaded yet
  const matched = to.matched.find((r) => r.meta.remoteName);
  if (!matched) return;

  const remoteName = matched.meta.remoteName as string;
  if (loadedRemotes.has(remoteName)) return;

  const loader = remoteLoaders[remoteName];
  if (!loader) return;

  const mod = await loader();

  for (const route of mod.routes) {
    router.addRoute(`mfe-${remoteName}`, route);
  }
  loadedRemotes.add(remoteName);

  // Re-navigate so the newly added child routes can match
  return to.fullPath;
});
