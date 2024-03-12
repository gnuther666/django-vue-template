<template>
  <div>
    <!-- 按钮组件 -->
    <el-button @click="handleDownload">点击下载图片</el-button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ServerUrl } from '@/http'
import { getTestImage } from '@/api'

const props = defineProps({
  api_url: String
})

// 假设这是从响应中获取的文件URL
const fileUrl = ref('')
const down_file_name = ref('')

async function handleDownload() {
  // 调用后端接口获取文件地址
  const url = ServerUrl + props.api_url
  console.log('请求路径', ServerUrl, props.api_url, url)
  getTestImage(url).then((res) => {
    console.log('下载结果', res)
    // 获取到文件URL
    if (res.data && res.data.file_path) {
      console.log('检查输入路径', ServerUrl, res.data.file_path)
      fileUrl.value = ServerUrl + res.data.file_path
      const tmp_file_name = res.data.file_path.split('/')
      down_file_name.value = tmp_file_name[tmp_file_name.length - 1]
      // 触发下载
      downloadFile()
    }
  })
}

function downloadFile() {
  fetch(fileUrl.value)
    .then((res) => {
      return res.arrayBuffer()
    })
    .then((fileContent) => {
      const blob = new Blob([fileContent])
      const reader = new FileReader()
      reader.onload = () => {
        const newUrl = reader.result
        const a = document.createElement('a')
        a.href = newUrl
        a.download = down_file_name.value
        a.click()
      }
      reader.readAsDataURL(blob)
    })
}

// 在组件挂载时确保DOM元素存在
onMounted(() => {
  // 如果需要的话，在这里可以做一些初始化工作
})
</script>
