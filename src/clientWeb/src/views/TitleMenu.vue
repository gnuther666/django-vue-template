<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import TopMenuUser from '@/views/TopMenuUser.vue'
const local_value = ref({
  activueIndex2: '1'
})

function handleSelect(key: string, keyPath: string[]) {
  console.log(key, keyPath)
}
</script>

<template>
  <div class="base_page">
    <el-container>
      <el-header style="padding: 0"
        ><el-menu
          :default-active="local_value.activeIndex2"
          class="el-menu-demo"
          mode="horizontal"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleSelect"
        >
          <div>
            <a href="/"
              ><img src="@/assets/image/project_logo.png" class="homepage_logo" alt=""
            /></a>
          </div>
          <el-menu-item index="1">首页</el-menu-item>
          <el-menu-item index="2">示例</el-menu-item>
          <div style="position: absolute; right: 0"><TopMenuUser /></div></el-menu
      ></el-header>
      <el-main><RouterView /></el-main>
    </el-container>
  </div>
</template>

<style>
.homepage_logo {
  height: 60%;
  position: relative;
  top: 20%;
  left: 20%;
  margin-right: 20px;
}
</style>
