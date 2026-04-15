import { createRouter, createWebHistory } from "vue-router";
import ItemListView from "../views/ItemListView.vue";

export const router = createRouter({
  history: createWebHistory("/apps/example1/"),
  routes: [
    {
      path: "/",
      redirect: "/items",
    },
    {
      path: "/items",
      name: "item-list",
      component: ItemListView,
    },
    {
      path: "/items/new",
      name: "item-create",
      component: () => import("../views/ItemCreateView.vue"),
    },
    {
      path: "/items/:id",
      name: "item-detail",
      component: () => import("../views/ItemDetailView.vue"),
    },
  ],
});
