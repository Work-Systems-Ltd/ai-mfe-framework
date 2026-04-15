import { createRouter, createWebHistory } from "vue-router";
import AppLayout from "../layouts/AppLayout.vue";
import DashboardView from "../views/DashboardView.vue";

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
          path: "app/:appName/:pathMatch(.*)*",
          name: "mfe-app",
          component: () => import("../views/AppView.vue"),
        },
      ],
    },
  ],
});
