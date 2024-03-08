<script setup lang="ts">
import { ref } from 'vue'

import imageList from '../components/ImageList.vue'

const local_value = ref({
  image_list: ['a.png', 'b.png']
})
</script>

<template>
  <main>
    <div>图片列表</div>
    <div><imageList :image_list="local_value.image_list" /></div>
  </main>
</template>
