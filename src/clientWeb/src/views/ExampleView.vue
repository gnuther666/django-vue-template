<script setup lang="ts">
import { getImageList } from '@/api'
import { ref, onMounted } from 'vue'
import ImageList from '@/components/ImageList.vue'

// // 创建一个响应式的状态来存储从接口获取的数据
const data = ref({
  image_list: [] as Array<any> // 根据实际数据类型指定类型
})

// // 定义一个要在页面加载时调用的函数
// onMounted(() => {
//   getImageList().then((res) => {
//     data.value.image_list = res.data
//   })
// })
onMounted(() => {
  console.log('初始化以下')
  getImageList().then((res) => {
    data.value.image_list = res.data.images
  })
})
</script>

<template>
  <main>
    <div>图片列表</div>
    <ImageList :image_list="data.image_list" />
  </main>
</template>
