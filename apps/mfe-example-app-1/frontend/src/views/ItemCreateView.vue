<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { apiFetch } from "@common/lib/api";

const router = useRouter();
const name = ref("");
const description = ref("");
const submitting = ref(false);

async function createItem(): Promise<void> {
  submitting.value = true;
  try {
    await apiFetch("/apps/example1/api/items", {
      method: "POST",
      body: JSON.stringify({ name: name.value, description: description.value }),
    });
    router.push("/items");
  } catch (error) {
    console.error("Failed to create item:", error);
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div>
    <button class="text-sm text-muted-foreground mb-4 hover:text-foreground" @click="router.back()">
      &larr; Back to items
    </button>

    <h1 class="text-xl font-bold mb-6">Create Item</h1>

    <form class="space-y-4 max-w-md" @submit.prevent="createItem">
      <div>
        <label class="block text-sm font-medium mb-1" for="name">Name</label>
        <input
          id="name"
          v-model="name"
          type="text"
          required
          class="w-full px-3 py-2 border rounded-md bg-background"
          placeholder="Item name"
        />
      </div>

      <div>
        <label class="block text-sm font-medium mb-1" for="description">Description</label>
        <textarea
          id="description"
          v-model="description"
          required
          rows="3"
          class="w-full px-3 py-2 border rounded-md bg-background"
          placeholder="Item description"
        />
      </div>

      <button
        type="submit"
        :disabled="submitting"
        class="px-4 py-2 bg-primary text-primary-foreground rounded-md text-sm hover:opacity-90 disabled:opacity-50"
      >
        {{ submitting ? "Creating..." : "Create Item" }}
      </button>
    </form>
  </div>
</template>
