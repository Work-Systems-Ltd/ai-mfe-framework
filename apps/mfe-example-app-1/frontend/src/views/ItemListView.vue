<script setup lang="ts">
import { ref, onMounted } from "vue";
import { apiFetch } from "@common/lib/api";

interface Item {
  id: string;
  name: string;
  description: string;
  owner_id: string;
}

const items = ref<Item[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    items.value = await apiFetch<Item[]>("/apps/example1/api/items");
  } catch (error) {
    console.error("Failed to fetch items:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold">Items</h1>
      <router-link
        to="/items/new"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm hover:opacity-90"
      >
        Create Item
      </router-link>
    </div>

    <div v-if="loading" class="text-muted-foreground">Loading items...</div>

    <div v-else-if="items.length === 0" class="text-center py-8 text-muted-foreground">
      No items yetsss. Create your first item!
    </div>

    <div v-else class="space-y-3">
      <router-link
        v-for="item in items"
        :key="item.id"
        :to="`/items/${item.id}`"
        class="block border rounded-lg p-4 hover:shadow-md transition-shadow"
      >
        <h3 class="font-medium">{{ item.name }}</h3>
        <p class="text-sm text-muted-foreground">{{ item.description }}</p>
      </router-link>
    </div>
  </div>
</template>
<!-- test Wed 15 Apr 2026 06:38:46 AM UTC -->
<!-- polling-test Wed 15 Apr 2026 06:40:20 AM UTC -->
<!-- HOST WRITE Wed 15 Apr 2026 06:45:12 AM UTC -->
<!-- POLL TEST Wed 15 Apr 2026 06:45:38 AM UTC -->
