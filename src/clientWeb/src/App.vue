<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app_page">
    <RouterView />
  </div>
</template>

<style scoped>
.base_page {
  width: 100vw;
  height: 99vh;
  display: flex;
}
</style>
