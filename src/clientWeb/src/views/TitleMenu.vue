<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TopMenuUser from '@/views/TopMenuUser.vue'
const local_value = ref({
  activueIndex2: '1',
  logoutDialogVisible: false
})
const router = useRouter()
const use_router = ref(true)
function handleSelect(key: string, keyPath: string[]) {
  if (key.startsWith('ignore_')) {
    console.log('不做处理')
  } else {
    router.push(key)
  }
}

function confirmLogout() {
  // 确认退出登录的逻辑，例如清除token、跳转到登录页面等
  localStorage.removeItem('access_token') // 假设token存放在localStorage
  router.push('/login')
  local_value.value.logoutDialogVisible = false
}

function showLogoutConfirm(event) {
  // event.preventDefault() // 阻止默认行为（如果需要的话）
  console.log('退出登录')
  local_value.value.logoutDialogVisible = true
}
</script>

<template>
  <div class="base_page">
    <el-container>
      <el-header style="padding: 0">
        <el-menu
          :default-active="$route.path"
          class="el-menu-demo"
          :router="use_router"
          mode="horizontal"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          @select="handleSelect"
          flex
        >
          <div>
            <a href="/"
              ><img src="@/assets/image/project_logo.png" class="homepage_logo" alt="" /><label
                style="margin-left: 10px; font-size: 20px; font-weight: bold; margin-right: 10px"
                >全栈模板系统前台</label
              ></a
            >
          </div>
          <el-menu-item index="/">首页</el-menu-item>
          <el-menu-item index="/example">示例</el-menu-item>
          <el-sub-menu index="ignore_submenu_1" style="position: absolute; right: 0"
            ><template #title><TopMenuUser /></template>
            <el-menu-item index="/user">用户中心</el-menu-item>
            <el-menu-item index="/help">帮助</el-menu-item>
            <el-menu-item index="/login" @click="showLogoutConfirm">退出登录</el-menu-item>
          </el-sub-menu>
          <!-- <div class="user_info_blck">
            <TopMenuUser /></div> -->
        </el-menu></el-header
      >
      <el-main><RouterView /></el-main>
      <el-dialog
        title="退出登录确认"
        v-model="local_value.logoutDialogVisible"
        width="30%"
        append-to-body
        style="z-index: 99"
      >
        <span>确定要退出登录吗？</span>
        <div slot="footer">
          <el-button @click="local_value.logoutDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmLogout">确定</el-button>
        </div>
      </el-dialog>
    </el-container>
  </div>
</template>

<style>
.homepage_logo {
  height: 60%;
  position: relative;
  top: 20%;
  left: 5%;
  margin-right: 20px;
}
.user_info_blck {
  position: absolute;
  right: 0;
  height: 100%;
  background-color: rgba(109, 118, 124, 0.5);
}
</style>
