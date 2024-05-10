<script setup lang="ts">
import { ServerUrl } from '@/api/base_http'

defineProps(['image_list'])
</script>

<template>
  <main>
    <el-row :gutter="10">
      <el-col
        v-for="(imageUrl, index) in image_list"
        :key="index"
        :xs="8"
        :sm="8"
        :md="8"
        :lg="6"
        :xl="2"
      >
        <el-image
          :src="`${ServerUrl}${imageUrl}`"
          fit="cover"
          style="height: 100px"
          alt="Image from list"
        >
        </el-image>
      </el-col>
    </el-row>
  </main>
</template>
