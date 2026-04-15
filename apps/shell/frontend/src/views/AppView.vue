<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import AppFrame from "../components/AppFrame.vue";

const route = useRoute();

const appName = computed(() => route.params.appName as string);
const subPath = computed(() => {
  const pathMatch = route.params.pathMatch;
  if (Array.isArray(pathMatch)) {
    return pathMatch.join("/");
  }
  return pathMatch ?? "";
});

const iframeSrc = computed(() => {
  const base = `/apps/${appName.value}/`;
  return subPath.value ? `${base}${subPath.value}` : base;
});
</script>

<template>
  <AppFrame :src="iframeSrc" />
</template>
