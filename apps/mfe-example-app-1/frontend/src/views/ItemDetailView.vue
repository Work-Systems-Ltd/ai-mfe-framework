<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { apiFetch } from "@common/lib/api";

interface Item {
  id: string;
  name: string;
  description: string;
  owner_id: string;
}

const route = useRoute();
const router = useRouter();
const item = ref<Item | null>(null);
const loading = ref(true);

onMounted(async () => {
  try {
    item.value = await apiFetch<Item>(`/apps/example1/api/items/${route.params.id}`);
  } catch {
    console.error("Item not found");
  } finally {
    loading.value = false;
  }
});

async function deleteItem(): Promise<void> {
  if (!item.value) return;
  try {
    await apiFetch(`/apps/example1/api/items/${item.value.id}`, { method: "DELETE" });
    router.push({ name: "example1-item-list" });
  } catch (error) {
    console.error("Failed to delete:", error);
  }
}
</script>

<template>
  <div>
    <button class="text-sm text-muted-foreground mb-4 hover:text-foreground" @click="router.back()">
      &larr; Back to items
    </button>

    <div v-if="loading" class="text-muted-foreground">Loading...</div>

    <div v-else-if="item" class="border rounded-lg p-6">
      <h1 class="text-xl font-bold mb-2">{{ item.name }}</h1>
      <p class="text-muted-foreground mb-4">{{ item.description }}</p>
      <p class="text-sm text-muted-foreground">Owner: {{ item.owner_id }}</p>

      <div class="mt-6 pt-4 border-t">
        <button
          class="px-4 py-2 bg-destructive text-destructive-foreground rounded-md text-sm hover:opacity-90"
          @click="deleteItem"
        >
          Delete Item
        </button>
      </div>
    </div>

    <div v-else class="text-muted-foreground">Item not found.</div>
  </div>
</template>
