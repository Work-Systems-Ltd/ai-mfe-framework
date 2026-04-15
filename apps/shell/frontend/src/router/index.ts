import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "../layouts/AppLayout.vue";
import DashboardView from "../views/DashboardView.vue";
import RemoteAppView from "../views/RemoteAppView.vue";

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
          component: RemoteAppView,
          children: [
            { path: "", redirect: "items" },
            {
              path: "items",
              name: "example1-item-list",
              component: () => import("example1/ItemListView").then((m) => m.default),
            },
            {
              path: "items/new",
              name: "example1-item-create",
              component: () => import("example1/ItemCreateView").then((m) => m.default),
            },
            {
              path: "items/:id",
              name: "example1-item-detail",
              component: () => import("example1/ItemDetailView").then((m) => m.default),
            },
          ],
        },
      ],
    },
  ],
});
