/**
 * Route definitions for the example app.
 * Exported for Module Federation — the shell imports these
 * and registers them as nested routes.
 */

import type { RouteRecordRaw } from "vue-router";
import ItemListView from "./views/ItemListView.vue";

export const routes: RouteRecordRaw[] = [
  {
    path: "",
    redirect: "items",
  },
  {
    path: "items",
    name: "example1-item-list",
    component: ItemListView,
  },
  {
    path: "items/new",
    name: "example1-item-create",
    component: () => import("./views/ItemCreateView.vue"),
  },
  {
    path: "items/:id",
    name: "example1-item-detail",
    component: () => import("./views/ItemDetailView.vue"),
  },
];
