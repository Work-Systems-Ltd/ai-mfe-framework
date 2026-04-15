<script setup lang="ts">
/**
 * Container for remote MFE app content.
 * The actual route matching happens via child routes
 * that are dynamically added by the router setup.
 */
</script>

<template>
  <div class="h-full overflow-auto p-8">
    <router-view />
  </div>
</template>
